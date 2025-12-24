// Copyright Epic Games, Inc. All Rights Reserved.

#include "ArenaGeometryImporter.h"
#include "Misc/FileHelper.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "ProceduralMeshComponent.h"
#include "Engine/Engine.h"

AArenaGeometryImporter::AArenaGeometryImporter()
{
	PrimaryActorTick.bCanEverTick = false;
	
	// Create root component
	USceneComponent* Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);
}

void AArenaGeometryImporter::BeginPlay()
{
	Super::BeginPlay();
	
	// Auto-import if path is set
	if (!JsonFilePath.IsEmpty())
	{
		ImportArenaFromJson(JsonFilePath);
	}
}

bool AArenaGeometryImporter::ImportArenaFromJson(const FString& FilePath)
{
	// Clear existing geometry
	ClearGeometry();
	
	// Read JSON file
	FString JsonContent;
	if (!FFileHelper::LoadFileToString(JsonContent, *FilePath))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to read JSON file: %s"), *FilePath);
		return false;
	}
	
	// Parse and create geometry
	if (ParseJsonGeometry(JsonContent))
	{
		UE_LOG(LogTemp, Log, TEXT("Successfully imported arena geometry from: %s"), *FilePath);
		return true;
	}
	
	return false;
}

bool AArenaGeometryImporter::ParseJsonGeometry(const FString& JsonContent)
{
	// Parse JSON
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonContent);
	
	if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to parse JSON content"));
		return false;
	}
	
	// Get meshes array
	const TArray<TSharedPtr<FJsonValue>>* MeshesArray;
	if (!JsonObject->TryGetArrayField(TEXT("meshes"), MeshesArray))
	{
		UE_LOG(LogTemp, Error, TEXT("No 'meshes' array found in JSON"));
		return false;
	}
	
	// Process each mesh
	for (const TSharedPtr<FJsonValue>& MeshValue : *MeshesArray)
	{
		TSharedPtr<FJsonObject> MeshObject = MeshValue->AsObject();
		if (!MeshObject.IsValid())
			continue;
		
		// Extract mesh name
		FString MeshName = MeshObject->GetStringField(TEXT("name"));
		
		// Extract vertices
		TArray<FVector> Vertices;
		const TArray<TSharedPtr<FJsonValue>>* VerticesArray;
		if (MeshObject->TryGetArrayField(TEXT("vertices"), VerticesArray))
		{
			for (const TSharedPtr<FJsonValue>& VertexValue : *VerticesArray)
			{
				const TArray<TSharedPtr<FJsonValue>>& VertexArray = VertexValue->AsArray();
				if (VertexArray.Num() >= 3)
				{
					FVector Vertex(
						VertexArray[0]->AsNumber(),
						VertexArray[1]->AsNumber(),
						VertexArray[2]->AsNumber()
					);
					Vertices.Add(Vertex);
				}
			}
		}
		
		// Extract triangles (flatten the tuples into a single array)
		TArray<int32> Triangles;
		const TArray<TSharedPtr<FJsonValue>>* TrianglesArray;
		if (MeshObject->TryGetArrayField(TEXT("triangles"), TrianglesArray))
		{
			for (const TSharedPtr<FJsonValue>& TriangleValue : *TrianglesArray)
			{
				const TArray<TSharedPtr<FJsonValue>>& TriangleArray = TriangleValue->AsArray();
				if (TriangleArray.Num() >= 3)
				{
					Triangles.Add(TriangleArray[0]->AsNumber());
					Triangles.Add(TriangleArray[1]->AsNumber());
					Triangles.Add(TriangleArray[2]->AsNumber());
				}
			}
		}
		
		// Extract UVs
		TArray<FVector2D> UVs;
		const TArray<TSharedPtr<FJsonValue>>* UVsArray;
		if (MeshObject->TryGetArrayField(TEXT("uvs"), UVsArray))
		{
			for (const TSharedPtr<FJsonValue>& UVValue : *UVsArray)
			{
				const TArray<TSharedPtr<FJsonValue>>& UVArray = UVValue->AsArray();
				if (UVArray.Num() >= 2)
				{
					FVector2D UV(
						UVArray[0]->AsNumber(),
						UVArray[1]->AsNumber()
					);
					UVs.Add(UV);
				}
			}
		}
		
		// Create the mesh
		if (Vertices.Num() > 0 && Triangles.Num() > 0)
		{
			CreateMeshFromData(MeshName, Vertices, Triangles, UVs);
		}
	}
	
	return GeneratedMeshes.Num() > 0;
}

UProceduralMeshComponent* AArenaGeometryImporter::CreateMeshFromData(
	const FString& MeshName,
	const TArray<FVector>& Vertices,
	const TArray<int32>& Triangles,
	const TArray<FVector2D>& UVs)
{
	// Create a new procedural mesh component
	UProceduralMeshComponent* MeshComponent = NewObject<UProceduralMeshComponent>(this, *MeshName);
	if (!MeshComponent)
		return nullptr;
	
	MeshComponent->RegisterComponent();
	MeshComponent->AttachToComponent(GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform);
	
	// Generate normals and tangents
	TArray<FVector> Normals;
	TArray<FProcMeshTangent> Tangents;
	TArray<FLinearColor> VertexColors;
	
	// Simple normal calculation (can be improved)
	Normals.SetNum(Vertices.Num());
	for (int32 i = 0; i < Normals.Num(); i++)
	{
		Normals[i] = FVector(0, 0, 1); // Default up normal
	}
	
	// Create the mesh section
	MeshComponent->CreateMeshSection_LinearColor(
		0,                    // Section index
		Vertices,            // Vertices
		Triangles,           // Triangles
		Normals,            // Normals
		UVs,                // UV0
		TArray<FVector2D>(), // UV1 (empty)
		TArray<FVector2D>(), // UV2 (empty)
		TArray<FVector2D>(), // UV3 (empty)
		VertexColors,       // Vertex colors
		Tangents,           // Tangents
		true                // Create collision
	);
	
	// Set material if available
	if (DefaultMaterial)
	{
		MeshComponent->SetMaterial(0, DefaultMaterial);
	}
	
	GeneratedMeshes.Add(MeshComponent);
	
	UE_LOG(LogTemp, Log, TEXT("Created mesh: %s with %d vertices and %d triangles"), 
		*MeshName, Vertices.Num(), Triangles.Num() / 3);
	
	return MeshComponent;
}

void AArenaGeometryImporter::ClearGeometry()
{
	for (UProceduralMeshComponent* Mesh : GeneratedMeshes)
	{
		if (Mesh)
		{
			Mesh->ClearAllMeshSections();
			Mesh->DestroyComponent();
		}
	}
	GeneratedMeshes.Empty();
}
