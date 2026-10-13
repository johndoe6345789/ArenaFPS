// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "AIController.h"
#include "ArenaBot.generated.h"

/**
 * Arena FPS Bot AI Controller
 * Implements basic bot behavior for arena-style FPS deathmatch
 */
UCLASS()
class ARENAFPSRUNTIME_API AArenaBot : public AAIController
{
	GENERATED_BODY()

public:
	AArenaBot();

	// Bot skill level (0-5, where 5 is nightmare)
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaFPS|Bot")
	int32 SkillLevel = 2;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaFPS|Bot")
	FString BotName = "Bot";

	// Combat settings
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaFPS|Combat")
	float AccuracyModifier = 0.7f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaFPS|Combat")
	float ReactionTime = 0.3f;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	// AI behavior functions
	UFUNCTION(BlueprintCallable, Category = "ArenaFPS|AI")
	void UpdateBehavior();

	UFUNCTION(BlueprintCallable, Category = "ArenaFPS|AI")
	AActor* FindNearestEnemy();

	UFUNCTION(BlueprintCallable, Category = "ArenaFPS|AI")
	AActor* FindNearestWeapon();

	UFUNCTION(BlueprintCallable, Category = "ArenaFPS|AI")
	AActor* FindNearestHealthPack();

	UFUNCTION(BlueprintCallable, Category = "ArenaFPS|AI")
	void MoveToTarget(AActor* Target);

private:
	enum class EBotState : uint8
	{
		Idle,
		SeekingWeapon,
		SeekingHealth,
		Combat,
		Roaming
	};

	EBotState CurrentState;
	AActor* CurrentTarget;
	float LastStateChangeTime;
};
