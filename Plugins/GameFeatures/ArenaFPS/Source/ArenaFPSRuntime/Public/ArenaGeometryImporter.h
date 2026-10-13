// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ProceduralMeshComponent.h"
#include "ArenaGeometryImporter.generated.h"

/**
 * Imports procedurally generated arena geometry from JSON
 * Can be used in Blueprint or C++ to load arena_geometry.json
 */
UCLASS(Blueprintable, BlueprintType)
class ARENAFPSRUNTIME_API AArenaGeometryImporter : public AActor
{
	GENERATED_BODY()

public:
	AArenaGeometryImporter();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Arena|Import")
	FString JsonFilePath;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Arena|Import")
	UMaterial* DefaultMaterial;

	UFUNCTION(BlueprintCallable, Category = "Arena|Import")
	bool ImportArenaFromJson(const FString& FilePath);

	UFUNCTION(BlueprintCallable, Category = "Arena|Import")
	void ClearGeometry();

protected:
	virtual void BeginPlay() override;

private:
	UPROPERTY()
	TArray<UProceduralMeshComponent*> GeneratedMeshes;

	bool ParseJsonGeometry(const FString& JsonContent);
	UProceduralMeshComponent* CreateMeshFromData(
		const FString& MeshName,
		const TArray<FVector>& Vertices,
		const TArray<int32>& Triangles,
		const TArray<FVector2D>& UVs
	);
};
