// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "Quake3GameMode.generated.h"

class AQuake3Bot;

/**
 * Quake 3 Arena Deathmatch Game Mode
 * Implements classic Q3A deathmatch rules with frag limit and time limit
 */
UCLASS()
class QUAKE3ARENARUNTIME_API AQuake3GameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AQuake3GameMode();

	// Game settings
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quake3|GameRules")
	int32 FragLimit = 25;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quake3|GameRules")
	float TimeLimit = 600.0f; // 10 minutes in seconds

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quake3|GameRules")
	int32 NumberOfBots = 3;

	// Respawn settings
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quake3|Respawn")
	float RespawnDelay = 3.0f;

protected:
	virtual void BeginPlay() override;
	virtual void PostLogin(APlayerController* NewPlayer) override;

	UFUNCTION(BlueprintCallable, Category = "Quake3")
	void SpawnBots();

	UFUNCTION(BlueprintCallable, Category = "Quake3")
	void OnPlayerKilled(AController* Killer, AController* Victim);

	UFUNCTION(BlueprintCallable, Category = "Quake3")
	bool CheckGameEnd();

private:
	UPROPERTY()
	TArray<AQuake3Bot*> BotList;

	float GameStartTime;
};
