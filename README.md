# ArenaFPS

Developed with Unreal Engine 5

## GitHub Actions diagnostics

Use `tools/workflow_diagnostics.py` to summarize and lint the repository's
GitHub Actions workflows without running any jobs. The script is dependency
free, but installing `pyyaml` enables deeper YAML parsing.

```bash
python tools/workflow_diagnostics.py
```

Pass `--root /path/to/repo` to inspect another checkout.
