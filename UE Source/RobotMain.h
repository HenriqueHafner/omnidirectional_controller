// Created by Henrique Hafner Ferreira

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "PhysicsEngine/PhysicsConstraintComponent.h"
#include "SocketUEPY.h"

#include "RobotMain.generated.h"


USTRUCT() // remover usar a lista de Ustatimesh
struct FRobotLinks // Custom Containner for robot links
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere)
	int16 id;
	UPROPERTY(EditAnywhere)
	FName name;
	UPROPERTY(EditAnywhere)
	FVector pose_translation = FVector::ZeroVector;
	UPROPERTY(EditAnywhere)
	FRotator pose_rotation = FRotator::ZeroRotator;
	UPROPERTY(EditAnywhere)
	FString model_path;
	UPROPERTY(EditAnywhere)
	UStaticMeshComponent* link_instance;
	UPROPERTY(EditAnywhere)
	USceneComponent* link_base;
};

USTRUCT() // remover usar a lista de Ustatimesh
struct FRobotJoints // Custom Containner for robot links
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere)
	int16 id;
	UPROPERTY(EditAnywhere)
	FName name;
	UPROPERTY(EditAnywhere)
	UPhysicsConstraintComponent* joint;
	UPROPERTY(EditAnywhere)
	FVector pose_translation = FVector::ZeroVector;
	UPROPERTY(EditAnywhere)
	FRotator pose_rotation = FRotator::ZeroRotator;
	UPROPERTY(EditAnywhere)
	uint16 link_base_id;
	UPROPERTY(EditAnywhere)
	uint16 link_reac_id;
	UPROPERTY(EditAnywhere)
	UStaticMeshComponent* link_base;
	UPROPERTY(EditAnywhere)
	UStaticMeshComponent* link_reac;
};

UCLASS()
class BOXBOT_API ARobotMain : public APawn
{
// Native from UE player class, start
	GENERATED_BODY()
public:
	ARobotMain();
protected:
	virtual void BeginPlay() override;
public:	
	virtual void Tick(float DeltaTime) override;
	virtual void OnConstruction(const FTransform& Transform) override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;
// Native from UE player class, End


// ####### Class Implementation #######
public: //Attributes
	UPROPERTY(VisibleAnywhere)
	TMap<uint16, FRobotLinks> Links_list;

	UPROPERTY(VisibleAnywhere)
	TMap<uint16, FRobotJoints> Joints_list;

	UPROPERTY(VisibleAnywhere)
	TArray<UStaticMeshComponent*> relevant_phys_components;

	UPROPERTY(VisibleAnywhere)
	TMap<uint16, UStaticMeshComponent*> Meshcomp_list;

	UPROPERTY(VisibleAnywhere)
	TMap<FString, UStaticMesh*> Models_list;

	uint16 link_identifier_counter = 10;
	uint16 joint_identifier_counter = 10;

	UPROPERTY(VisibleAnywhere)
	TSet<FName> subconponent_all_used_nameid;

public: // Methods
	//Links
	bool link_create_all();
	void create_mesh_dictionary(const TArray<FString>& mesh_paths);
	uint16 link_add(FName name_input, FString model_path_input);
	bool link_setup(
		uint16 link_id,
		 FVector translator = FVector::ZeroVector,
		  FRotator rotator = FRotator::ZeroRotator );
	//Joints
	bool joint_create_all();
	uint16 joint_add(FName name_input);
	bool joint_revolute_setup(
		uint16 joint_id,
		 FVector free_axis_vector,
		  uint8 link_A_ID,
		   uint8 link_B_ID,
		    FVector relative_location,
		     FRotator relative_rotator);
	bool joint_setup_motor(uint16 joint_ID);

	//Interface
	void setup_socket();
	void python_call_handler();

public: // objects
	UPROPERTY(EditAnywhere) USceneComponent*
	root_component;
	USocketUEPY* SocketSubComp;
	FTimerHandle timer_call_handler;
};
