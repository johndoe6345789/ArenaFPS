// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "AIController.h"
#include "Quake3Bot.generated.h"

/**
 * Quake 3 Bot AI Controller (Crash Bot)
 * Implements basic bot behavior for Quake 3 Arena deathmatch
 */
UCLASS()
class QUAKE3ARENARUNTIME_API AQuake3Bot : public AAIController
{
	GENERATED_BODY()

public:
	AQuake3Bot();

	// Bot skill level (0-5, where 5 is nightmare)
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quake3|Bot")
	int32 SkillLevel = 2;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quake3|Bot")
	FString BotName = "Crash";

	// Combat settings
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quake3|Combat")
	float AccuracyModifier = 0.7f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quake3|Combat")
	float ReactionTime = 0.3f;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	// AI behavior functions
	UFUNCTION(BlueprintCallable, Category = "Quake3|AI")
	void UpdateBehavior();

	UFUNCTION(BlueprintCallable, Category = "Quake3|AI")
	AActor* FindNearestEnemy();

	UFUNCTION(BlueprintCallable, Category = "Quake3|AI")
	AActor* FindNearestWeapon();

	UFUNCTION(BlueprintCallable, Category = "Quake3|AI")
	AActor* FindNearestHealthPack();

	UFUNCTION(BlueprintCallable, Category = "Quake3|AI")
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
