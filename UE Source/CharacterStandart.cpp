// Fill out your copyright notice in the Description page of Project Settings.


#include "CharacterStandart.h"

// Sets default values
ACharacterStandart::ACharacterStandart()
{
 	// Set this character to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

}

// Called when the game starts or when spawned
void ACharacterStandart::BeginPlay()
{
	Super::BeginPlay();
	
}

// Called every frame
void ACharacterStandart::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

// Called to bind functionality to input
void ACharacterStandart::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

}

