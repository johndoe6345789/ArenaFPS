"""Utilities to summarize and sanity-check GitHub Actions workflows.

This module is designed for ChatGPT/Codex agents that need a quick view of
workflow configuration without triggering network calls or needing to execute
any jobs.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowIssue:
    """Represents a single diagnostic finding."""

    level: str
    message: str
    context: Optional[str] = None


@dataclass
class WorkflowSummary:
    """Container for a workflow file summary and any discovered issues."""

    path: Path
    name: str
    events: List[str] = field(default_factory=list)
    jobs: List[str] = field(default_factory=list)
    issues: List[WorkflowIssue] = field(default_factory=list)
    parsed: bool = False


class WorkflowDiagnostics:
    """Inspect GitHub Actions workflow files for common pitfalls."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.workflows_dir = self.root / ".github" / "workflows"
        self.yaml = self._import_yaml()

    def _import_yaml(self) -> Optional[Any]:
        """Attempt to import PyYAML if available.

        The import is optional so the tool can still run in restricted
        environments. If PyYAML is missing we fall back to string-based
        diagnostics.
        """

        spec = importlib.util.find_spec("yaml")
        if spec is None:
            return None
        return importlib.import_module("yaml")

    def run(self) -> List[WorkflowSummary]:
        summaries: List[WorkflowSummary] = []
        if not self.workflows_dir.exists():
            return [WorkflowSummary(
                path=self.workflows_dir,
                name="(missing)",
                issues=[
                    WorkflowIssue(
                        level="error",
                        message="Workflow directory .github/workflows does not exist."
                    )
                ],
            )]

        for workflow_file in sorted(self.workflows_dir.glob("*.yml")):
            summaries.append(self._inspect_workflow(workflow_file))
        for workflow_file in sorted(self.workflows_dir.glob("*.yaml")):
            summaries.append(self._inspect_workflow(workflow_file))

        if not summaries:
            summaries.append(WorkflowSummary(
                path=self.workflows_dir,
                name="(empty)",
                issues=[WorkflowIssue(level="warning", message="No workflow files found.")],
            ))
        return summaries

    def _inspect_workflow(self, workflow_file: Path) -> WorkflowSummary:
        summary = WorkflowSummary(path=workflow_file, name=workflow_file.name)
        raw_text = workflow_file.read_text(encoding="utf-8")
        parsed = self._load_yaml(workflow_file, raw_text)
        if parsed is None:
            summary.issues.append(
                WorkflowIssue(
                    level="warning",
                    message="Could not parse YAML; limited diagnostics shown.",
                    context="Install pyyaml for richer analysis.",
                )
            )
            summary.issues.extend(self._string_based_issues(raw_text))
            return summary

        summary.parsed = True
        summary.name = parsed.get("name", workflow_file.name)
        summary.events = self._extract_events(parsed)
        summary.jobs = list(parsed.get("jobs", {}).keys())
        summary.issues.extend(self._job_issues(parsed))
        summary.issues.extend(self._permissions_issues(parsed))
        summary.issues.extend(self._checkout_issues(parsed))
        return summary

    def _load_yaml(self, workflow_file: Path, raw_text: str) -> Optional[Dict[str, Any]]:
        if self.yaml is None:
            return None

        try:
            loaded = self.yaml.safe_load(raw_text)
        except Exception as exc:
            return None

        if not isinstance(loaded, dict):
            return None
        return loaded

    def _extract_events(self, parsed: Dict[str, Any]) -> List[str]:
        triggers = parsed.get("on", [])
        if isinstance(triggers, dict):
            return list(triggers.keys())
        if isinstance(triggers, list):
            return list(triggers)
        if isinstance(triggers, str):
            return [triggers]
        return []

    def _job_issues(self, parsed: Dict[str, Any]) -> List[WorkflowIssue]:
        issues: List[WorkflowIssue] = []
        jobs = parsed.get("jobs")
        if not jobs:
            issues.append(WorkflowIssue(level="error", message="Workflow defines no jobs."))
            return issues

        for job_name, job_body in jobs.items():
            if not isinstance(job_body, dict):
                issues.append(
                    WorkflowIssue(
                        level="error",
                        message="Job body is not a mapping.",
                        context=job_name,
                    )
                )
                continue

            if "runs-on" not in job_body:
                issues.append(
                    WorkflowIssue(
                        level="error",
                        message="Job missing runs-on key.",
                        context=job_name,
                    )
                )
            steps = job_body.get("steps", [])
            if not steps:
                issues.append(
                    WorkflowIssue(
                        level="warning",
                        message="Job has no steps defined.",
                        context=job_name,
                    )
                )
        return issues

    def _permissions_issues(self, parsed: Dict[str, Any]) -> List[WorkflowIssue]:
        issues: List[WorkflowIssue] = []
        permissions = parsed.get("permissions")
        if permissions is None:
            issues.append(
                WorkflowIssue(
                    level="info",
                    message="No explicit permissions block; defaults will apply.",
                )
            )
        return issues

    def _checkout_issues(self, parsed: Dict[str, Any]) -> List[WorkflowIssue]:
        issues: List[WorkflowIssue] = []
        jobs = parsed.get("jobs", {}) or {}
        for job_name, job_body in jobs.items():
            steps = job_body.get("steps", []) if isinstance(job_body, dict) else []
            for step in steps:
                if not isinstance(step, dict):
                    continue
                uses = step.get("uses", "")
                if isinstance(uses, str) and uses.startswith("actions/checkout"):
                    if "@" not in uses:
                        issues.append(
                            WorkflowIssue(
                                level="warning",
                                message="actions/checkout not pinned to a version.",
                                context=job_name,
                            )
                        )
        return issues

    def _string_based_issues(self, raw_text: str) -> List[WorkflowIssue]:
        issues: List[WorkflowIssue] = []
        if "jobs:" not in raw_text:
            issues.append(WorkflowIssue(level="error", message="No jobs block detected."))
        if "on:" not in raw_text:
            issues.append(WorkflowIssue(level="warning", message="No on trigger detected."))
        return issues


def summarize_to_text(summaries: List[WorkflowSummary]) -> str:
    report: Dict[str, Any] = {
        "workflows": [
            {
                "path": str(summary.path),
                "name": summary.name,
                "events": summary.events,
                "jobs": summary.jobs,
                "issues": [
                    {
                        "level": issue.level,
                        "message": issue.message,
                        **({"context": issue.context} if issue.context else {}),
                    }
                    for issue in summary.issues
                ],
                "parsed": summary.parsed,
            }
            for summary in summaries
        ]
    }
    return json.dumps(report, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose GitHub Actions workflows.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (defaults to current working directory).",
    )
    args = parser.parse_args()

    diagnostics = WorkflowDiagnostics(args.root)
    summaries = diagnostics.run()
    print(summarize_to_text(summaries))


if __name__ == "__main__":
    main()
