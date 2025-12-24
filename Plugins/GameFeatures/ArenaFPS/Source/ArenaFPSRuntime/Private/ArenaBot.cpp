// Copyright Epic Games, Inc. All Rights Reserved.

#include "ArenaBot.h"
#include "GameFramework/Character.h"
#include "Kismet/GameplayStatics.h"
#include "NavigationSystem.h"
#include "NavigationPath.h"

AArenaBot::AArenaBot()
{
	PrimaryActorTick.bCanEverTick = true;
	CurrentState = EBotState::Idle;
	CurrentTarget = nullptr;
	LastStateChangeTime = 0.0f;
}

void AArenaBot::BeginPlay()
{
	Super::BeginPlay();
	
	// Initialize bot
	CurrentState = EBotState::Roaming;
}

void AArenaBot::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	
	UpdateBehavior();
}

void AArenaBot::UpdateBehavior()
{
	if (!GetPawn())
	{
		return;
	}

	// Simple state machine for bot behavior
	switch (CurrentState)
	{
		case EBotState::Idle:
			// Look for something to do
			if (AActor* Enemy = FindNearestEnemy())
			{
				CurrentState = EBotState::Combat;
				CurrentTarget = Enemy;
			}
			else if (AActor* Weapon = FindNearestWeapon())
			{
				CurrentState = EBotState::SeekingWeapon;
				CurrentTarget = Weapon;
			}
			else
			{
				CurrentState = EBotState::Roaming;
			}
			break;

		case EBotState::Combat:
			// Combat logic
			if (CurrentTarget && !CurrentTarget->IsPendingKill())
			{
				MoveToTarget(CurrentTarget);
				// Aim and shoot logic would go here
			}
			else
			{
				CurrentState = EBotState::Idle;
				CurrentTarget = nullptr;
			}
			break;

		case EBotState::SeekingWeapon:
			// Move to weapon pickup
			if (CurrentTarget && !CurrentTarget->IsPendingKill())
			{
				MoveToTarget(CurrentTarget);
			}
			else
			{
				CurrentState = EBotState::Idle;
				CurrentTarget = nullptr;
			}
			break;

		case EBotState::SeekingHealth:
			// Move to health pickup
			if (CurrentTarget && !CurrentTarget->IsPendingKill())
			{
				MoveToTarget(CurrentTarget);
			}
			else
			{
				CurrentState = EBotState::Idle;
				CurrentTarget = nullptr;
			}
			break;

		case EBotState::Roaming:
			// Random movement
			if (AActor* Enemy = FindNearestEnemy())
			{
				CurrentState = EBotState::Combat;
				CurrentTarget = Enemy;
			}
			else
			{
				// Move to random location
				if (UNavigationSystemV1* NavSys = UNavigationSystemV1::GetCurrent(GetWorld()))
				{
					FNavLocation RandomLocation;
					if (NavSys->GetRandomPointInNavigableRadius(GetPawn()->GetActorLocation(), 2000.0f, RandomLocation))
					{
						MoveToLocation(RandomLocation.Location);
					}
				}
			}
			break;
	}
}

AActor* AArenaBot::FindNearestEnemy()
{
	// Find all pawns and return the nearest one that isn't us
	TArray<AActor*> AllPawns;
	UGameplayStatics::GetAllActorsOfClass(GetWorld(), ACharacter::StaticClass(), AllPawns);

	AActor* NearestEnemy = nullptr;
	float NearestDistance = FLT_MAX;

	FVector MyLocation = GetPawn() ? GetPawn()->GetActorLocation() : FVector::ZeroVector;

	for (AActor* Actor : AllPawns)
	{
		if (Actor != GetPawn())
		{
			float Distance = FVector::Dist(MyLocation, Actor->GetActorLocation());
			if (Distance < NearestDistance)
			{
				NearestDistance = Distance;
				NearestEnemy = Actor;
			}
		}
	}

	return NearestEnemy;
}

AActor* AArenaBot::FindNearestWeapon()
{
	// This would find weapon pickups in the level
	// Placeholder for now
	return nullptr;
}

AActor* AArenaBot::FindNearestHealthPack()
{
	// This would find health pickups in the level
	// Placeholder for now
	return nullptr;
}

void AArenaBot::MoveToTarget(AActor* Target)
{
	if (Target)
	{
		MoveToActor(Target, 100.0f); // Get within 100 units of target
	}
}
