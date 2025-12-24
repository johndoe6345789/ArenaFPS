// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class Quake3ArenaRuntime : ModuleRules
{
	public Quake3ArenaRuntime(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"CoreUObject",
				"Engine",
				"ModularGameplay",
				"GameFeatures",
				"GameplayAbilities",
				"GameplayTags",
				"GameplayTasks",
				"ProceduralMeshComponent",
				"Json",
				"JsonUtilities",
			}
		);

		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"LyraGame",
				"NetCore",
				"EnhancedInput",
				"AIModule",
				"NavigationSystem",
				"GameplayMessageRuntime",
				"GeometryScriptingCore",
				"DynamicMesh",
			}
		);
	}
}
