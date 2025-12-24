// Copyright Epic Games, Inc. All Rights Reserved.

#include "Quake3GameMode.h"
#include "Quake3Bot.h"
#include "GameFramework/PlayerStart.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"

AQuake3GameMode::AQuake3GameMode()
{
	GameStartTime = 0.0f;
}

void AQuake3GameMode::BeginPlay()
{
	Super::BeginPlay();
	
	GameStartTime = GetWorld()->GetTimeSeconds();
	
	// Spawn bots after a short delay
	FTimerHandle SpawnTimerHandle;
	GetWorld()->GetTimerManager().SetTimer(SpawnTimerHandle, this, &AQuake3GameMode::SpawnBots, 1.0f, false);
}

void AQuake3GameMode::PostLogin(APlayerController* NewPlayer)
{
	Super::PostLogin(NewPlayer);
	
	// Player spawned, initialize their score
}

void AQuake3GameMode::SpawnBots()
{
	// Find all player starts
	TArray<AActor*> PlayerStarts;
	UGameplayStatics::GetAllActorsOfClass(GetWorld(), APlayerStart::StaticClass(), PlayerStarts);

	if (PlayerStarts.Num() == 0)
	{
		UE_LOG(LogTemp, Warning, TEXT("No player starts found in level!"));
		return;
	}

	// Spawn the requested number of bots
	for (int32 i = 0; i < NumberOfBots && i < PlayerStarts.Num(); ++i)
	{
		FActorSpawnParameters SpawnParams;
		SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;

		APlayerStart* SpawnPoint = Cast<APlayerStart>(PlayerStarts[i]);
		if (SpawnPoint)
		{
			// Bot spawning will be implemented when we have the bot class
			// For now, this is a placeholder
		}
	}
}

void AQuake3GameMode::OnPlayerKilled(AController* Killer, AController* Victim)
{
	// Increment killer's score
	if (Killer && Killer != Victim)
	{
		// Score tracking will be added
	}

	// Check if game should end
	CheckGameEnd();

	// Schedule respawn for victim
	if (Victim)
	{
		FTimerHandle RespawnTimerHandle;
		// Respawn logic will be added
	}
}

bool AQuake3GameMode::CheckGameEnd()
{
	// Check frag limit
	// This will be implemented with proper score tracking

	// Check time limit
	float ElapsedTime = GetWorld()->GetTimeSeconds() - GameStartTime;
	if (TimeLimit > 0 && ElapsedTime >= TimeLimit)
	{
		// End game
		return true;
	}

	return false;
}
