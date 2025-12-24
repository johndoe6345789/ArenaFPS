// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "ArenaGameMode.generated.h"

class AArenaBot;

/**
 * Arena FPS Deathmatch Game Mode
 * Implements classic arena-style FPS deathmatch rules with frag limit and time limit
 */
UCLASS()
class ARENAFPSRUNTIME_API AArenaGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AArenaGameMode();

	// Game settings
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaFPS|GameRules")
	int32 FragLimit = 25;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaFPS|GameRules")
	float TimeLimit = 600.0f; // 10 minutes in seconds

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaFPS|GameRules")
	int32 NumberOfBots = 3;

	// Respawn settings
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaFPS|Respawn")
	float RespawnDelay = 3.0f;

protected:
	virtual void BeginPlay() override;
	virtual void PostLogin(APlayerController* NewPlayer) override;

	UFUNCTION(BlueprintCallable, Category = "ArenaFPS")
	void SpawnBots();

	UFUNCTION(BlueprintCallable, Category = "ArenaFPS")
	void OnPlayerKilled(AController* Killer, AController* Victim);

	UFUNCTION(BlueprintCallable, Category = "ArenaFPS")
	bool CheckGameEnd();

private:
	UPROPERTY()
	TArray<AArenaBot*> BotList;

	float GameStartTime;
};
