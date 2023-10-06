// Created by Henrique Hafner Ferreira
#include "RobotMain.h"

/*
Talvez seja possível, no runtime, acessar o objeto de physica physx, e talvem desbravar a implementação da api diretamente.
perguntar para suporte do UE
*/

void ARobotMain::OnConstruction(const FTransform& Transform)
{
    Super::OnConstruction(Transform);
    FVector InitialLocation = FVector(-390.0f, -170.0f, 50.0f);
    SetActorLocation(InitialLocation);
}

ARobotMain::ARobotMain()
{
	PrimaryActorTick.bCanEverTick = true;

	//creating a root component to serve as base frame to place robot Links
	root_component = CreateDefaultSubobject<USceneComponent>(TEXT("root_component"));
	SetRootComponent(root_component);
	root_component->SetMobility(EComponentMobility::Movable);

	//Links
	link_create_all();
	//Joints
	joint_create_all();
	//Motors

	//Interface
	SocketSubComp = CreateDefaultSubobject<USocketUEPY>(TEXT("SocketObject"));

}

void ARobotMain::BeginPlay()
{
	Super::BeginPlay();
	setup_socket();
}

void ARobotMain::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	for (int32 Index = 0; Index < relevant_phys_components.Num(); Index++)
	{
		UStaticMeshComponent* MeshComponent = relevant_phys_components[Index];
		MeshComponent->GetBodyInstance()->WakeInstance();
	}
	if (SocketSubComp->is_connected) {
		python_call_handler();
	}
}

void ARobotMain::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    Super::EndPlay(EndPlayReason);
    GetWorldTimerManager().ClearTimer(timer_call_handler);
}

void ARobotMain::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

}

bool ARobotMain::link_create_all()
{
	TArray<FString> mesh_paths;
	mesh_paths.Add(TEXT("/Game/boxbot_custom/meshes/base"));
	mesh_paths.Add(TEXT("/Game/boxbot_custom/meshes/tower"));
	mesh_paths.Add(TEXT("/Game/boxbot_custom/meshes/wheel"));
	create_mesh_dictionary(mesh_paths);
	//Links
	uint16 ID;
	FVector  translator = FVector(0.0f, 0.0f, 0.0f);
	FRotator rotator	= FRotator(0.0f, 0.0f, 0.0f);
	//link1
	ID = link_add(TEXT("RobotBase"), TEXT("/Game/boxbot_custom/meshes/base"));
	translator = FVector(0.0f, 0.0f, 0.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	link_setup(ID, translator, rotator);
	//link2
	ID = link_add(TEXT("RobotActiveTowerFR"), TEXT("/Game/boxbot_custom/meshes/tower"));
	translator = FVector(63.5f, 58.32f, 0.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	link_setup(ID, translator, rotator);
	//link3
	translator = FVector(63.5f, 58.32f, 0.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = link_add(TEXT("RobotActuatedTireFR"), TEXT("/Game/boxbot_custom/meshes/wheel"));
	link_setup(ID, translator, rotator);
	//link4
	ID = link_add(TEXT("RobotActiveTowerFL"), TEXT("/Game/boxbot_custom/meshes/tower"));
	translator = FVector(-63.5f, 58.32f, 0.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	link_setup(ID, translator, rotator);
	//link5
	translator = FVector(-63.5f, 58.32f, 0.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = link_add(TEXT("RobotActuatedTireFL"), TEXT("/Game/boxbot_custom/meshes/wheel"));
	link_setup(ID, translator, rotator);
	//link6
	ID = link_add(TEXT("RobotActiveTowerRR"), TEXT("/Game/boxbot_custom/meshes/tower"));
	translator = FVector(63.5f, -58.32f, 0.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	link_setup(ID, translator, rotator);
	//link7
	translator = FVector(63.5f, -58.32f, 0.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = link_add(TEXT("RobotActuatedTireRR"), TEXT("/Game/boxbot_custom/meshes/wheel"));
	link_setup(ID, translator, rotator);
	//link8
	ID = link_add(TEXT("RobotActiveTowerRL"), TEXT("/Game/boxbot_custom/meshes/tower"));
	translator = FVector(-63.5f, -58.32f, 0.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	link_setup(ID, translator, rotator);
	//link9
	translator = FVector(-63.5f, -58.32f, 0.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = link_add(TEXT("RobotActuatedTireRL"), TEXT("/Game/boxbot_custom/meshes/wheel"));
	link_setup(ID, translator, rotator);
	return true;
}

bool ARobotMain::joint_create_all()
{
	uint16 ID;	
	FVector  translator;
	FRotator rotator;
	FVector free_direction;
	uint8 link_ID_reaction;
	uint8 link_ID_actuation;

	translator = FVector(63.5f, 58.32f, 20.5f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = joint_add(TEXT("JointSteeringTowerFR"));
	free_direction = FVector(0.0f, 0.0f, 1.0f);
	link_ID_reaction  = 10;
	link_ID_actuation = 11;
	joint_revolute_setup(ID, free_direction, link_ID_reaction, link_ID_actuation, translator, rotator);
	joint_setup_motor(ID);

	translator = FVector(-63.5f, 58.32f, 20.5f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = joint_add(TEXT("JointSteeringTowerFL"));
	free_direction = FVector(0.0f, 0.0f, 1.0f);
	link_ID_reaction  = 10;
	link_ID_actuation = 13;
	joint_revolute_setup(ID, free_direction, link_ID_reaction, link_ID_actuation, translator, rotator);
	joint_setup_motor(ID);

	translator = FVector(63.5f, -58.32f, 20.5f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = joint_add(TEXT("JointSteeringTowerRR"));
	free_direction = FVector(0.0f, 0.0f, 1.0f);
	link_ID_reaction  = 10;
	link_ID_actuation = 15;
	joint_revolute_setup(ID, free_direction, link_ID_reaction, link_ID_actuation, translator, rotator);
	joint_setup_motor(ID);

	translator = FVector(-63.5f, -58.32f, 20.5f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = joint_add(TEXT("JointSteeringTowerRL"));
	free_direction = FVector(0.0f, 0.0f, 1.0f);
	link_ID_reaction  = 10;
	link_ID_actuation = 17;
	joint_revolute_setup(ID, free_direction, link_ID_reaction, link_ID_actuation, translator, rotator);
	joint_setup_motor(ID);

	translator = FVector(0.0f, 0.0f, 10.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = joint_add(TEXT("JointWheelTractionFR"));
	free_direction = FVector(1.0f, 0.0f, 0.0f);
	link_ID_reaction  = 11;
	link_ID_actuation = 12;
	joint_revolute_setup(ID, free_direction, link_ID_reaction, link_ID_actuation, translator, rotator);
	joint_setup_motor(ID);

	translator = FVector(0.0f, 0.0f, 10.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = joint_add(TEXT("JointWheelTractionFL"));
	free_direction = FVector(1.0f, 0.0f, 0.0f);
	link_ID_reaction  = 13;
	link_ID_actuation = 14;
	joint_revolute_setup(ID, free_direction, link_ID_reaction, link_ID_actuation, translator, rotator);
	joint_setup_motor(ID);

	translator = FVector(0.0f, 0.0f, 10.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = joint_add(TEXT("JointWheelTractionRR"));
	free_direction = FVector(1.0f, 0.0f, 0.0f);
	link_ID_reaction  = 15;
	link_ID_actuation = 16;
	joint_revolute_setup(ID, free_direction, link_ID_reaction, link_ID_actuation, translator, rotator);
	joint_setup_motor(ID);

	translator = FVector(0.0f, 0.0f, 10.0f);
	rotator	= FRotator(0.0f, 0.0f, 0.0f);
	ID = joint_add(TEXT("JointWheelTractionRL"));
	free_direction = FVector(1.0f, 0.0f, 0.0f);
	link_ID_reaction  = 17;
	link_ID_actuation = 18;
	joint_revolute_setup(ID, free_direction, link_ID_reaction, link_ID_actuation, translator, rotator);
	joint_setup_motor(ID);

	return true;
}

uint16 ARobotMain::link_add(FName name_input, FString model_path_input)
{
	uint16 link_id = link_identifier_counter; // unique link identifier
	FString link_id_string = FString::Printf(TEXT("%d"), link_id); // String conversion of ID number
	FName nameid = FName(*(name_input.ToString() + "_" + link_id_string)); // name and id, concatenated
	if (subconponent_all_used_nameid.Contains(nameid))
	{
		UE_LOG(LogTemp, Error, TEXT("Name %s has already been used."), *nameid.ToString());
		// Retorne um valor adequado ou lide com o erro de outra forma
		return 0;
	}
	subconponent_all_used_nameid.Add(nameid);
	link_identifier_counter += 1;
	UPROPERTY(VisibleAnywhere)
	UStaticMeshComponent* Link = CreateDefaultSubobject<UStaticMeshComponent>(nameid); // link representation in UE SubOject
	if (Link != nullptr) {
		Meshcomp_list.Add(link_id, Link);
	}
	UStaticMesh* MeshToUse = Models_list.FindRef(model_path_input); // Model mesh for link
	if (MeshToUse)
	{
		Link->SetStaticMesh(MeshToUse);
	} else {
		UE_LOG(LogTemp, Error, TEXT("Mesh path not found in dictionary: %s"), *model_path_input);
	}
	FRobotLinks newLink;
	newLink.id = link_id;
	newLink.name = nameid;
	newLink.model_path = model_path_input;
	newLink.link_instance = Link;
	relevant_phys_components.Add(Link);	
	if (root_component) {
		newLink.link_base = root_component;
	} else {
		newLink.link_base = RootComponent;
	}
	Links_list.Add(link_id, newLink);
	return link_id;
}

bool ARobotMain::link_setup(uint16 link_id, FVector translator, FRotator rotator )
{
if (Links_list.Contains(link_id)) {
    FRobotLinks* Link = Links_list.Find(link_id);
    if (Link) {
		Link->pose_translation = translator;
		Link->pose_rotation = rotator;
		UStaticMeshComponent* LinkMeshComponent = Link->link_instance;
		LinkMeshComponent->SetupAttachment(Link->link_base);
		LinkMeshComponent->SetRelativeLocation(Link->pose_translation);
		LinkMeshComponent->SetRelativeRotation(Link->pose_rotation);
		LinkMeshComponent->SetMobility(EComponentMobility::Movable);
		LinkMeshComponent->SetSimulatePhysics(true);
		LinkMeshComponent->SetConstraintMode(EDOFMode::SixDOF);
		LinkMeshComponent->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Ignore);
		LinkMeshComponent->SetCollisionResponseToChannel(ECollisionChannel::ECC_WorldStatic, ECollisionResponse::ECR_Block);
		LinkMeshComponent->SetEnableGravity(true);
		LinkMeshComponent->GetBodyInstance()->AngularDamping = 1.0f;
		LinkMeshComponent->GetBodyInstance()->LinearDamping = 1.0f;
		LinkMeshComponent->GetBodyInstance()->UpdateInstanceSimulatePhysics();
	} else {
		return false;
	}
} else {
	return false;
	}
return false;
}

uint16 ARobotMain::joint_add(FName name_input)
{
	uint16 joint_id = joint_identifier_counter; // unique link identifier
	FString joint_id_string = FString::Printf(TEXT("%d"), joint_id); // String conversion of ID number
	FName nameid = FName(*(name_input.ToString() + "_" + joint_id_string)); // name and id, concatenated
	if (subconponent_all_used_nameid.Contains(nameid)) {
		UE_LOG(LogTemp, Error, TEXT("Name %s has already been used."), *nameid.ToString());
		return 0;}
	subconponent_all_used_nameid.Add(nameid);
	joint_identifier_counter += 1;
	FRobotJoints new_joint;
	new_joint.id = joint_id;
	new_joint.name = nameid;
	new_joint.pose_translation = FVector::ZeroVector;
	new_joint.pose_rotation = FRotator::ZeroRotator;
	new_joint.link_base_id = 0;
	new_joint.link_reac_id = 0;
	new_joint.link_base = nullptr;
	new_joint.link_reac = nullptr;
	new_joint.joint = CreateDefaultSubobject<UPhysicsConstraintComponent>(nameid); // UE constrain subcomponent pointer from last CreateDefaultSubobject
	Joints_list.Add(joint_id, new_joint);
	return joint_id;
}

bool ARobotMain::joint_revolute_setup(uint16 joint_id, FVector free_axis_vector, uint8 link_A_ID, uint8 link_B_ID, FVector relative_location, FRotator relative_rotator) {
	if (!Joints_list.Contains(joint_id)) {
		UE_LOG(LogTemp, Error, TEXT("Unable to find joint ID to setup."));
		return false; }
	FRobotJoints* joint_data = Joints_list.Find(joint_id);
	if (joint_data == nullptr) {
		UE_LOG(LogTemp, Error, TEXT("Unable to find joint ID to setup."));
		return false; }
	UPhysicsConstraintComponent* constrain = joint_data->joint;
	if (constrain == nullptr) {
		UE_LOG(LogTemp, Error, TEXT("Unable to find joint ID to setup."));
		return false; }
	// Check links IDs
	UStaticMeshComponent* link_A;
	UStaticMeshComponent* link_B;
	link_A = nullptr;
	link_B = nullptr;
	if (Links_list.Contains(link_A_ID)) {
		link_A = Links_list.Find(link_A_ID)->link_instance; }
	if (Links_list.Contains(link_A_ID)) {
		link_B = Links_list.Find(link_B_ID)->link_instance; }
	if ( (link_A == nullptr) || ((link_B == nullptr)) ) { // tentar attach com body ou no begin play
		UE_LOG(LogTemp, Error, TEXT("Error finding link by ID in order to attach it to the subcomponent."));
		return false; }
	// defining components to attach
	joint_data->link_base_id = link_A_ID;
	joint_data->link_reac_id = link_B_ID;
	joint_data->link_base = link_A;
	joint_data->link_reac = link_B;
	// defining assembly transformations
	joint_data->pose_translation = relative_location;
	FRotator align_twist = free_axis_vector.GetSafeNormal().Rotation(); // align the free Twist axis of the constrain to the required vectorial direction.
	FRotator combined_rotator = relative_rotator + align_twist;
	joint_data->pose_rotation = combined_rotator;
	// set the transformations
	constrain->SetRelativeLocation(relative_location);
	constrain->SetRelativeRotation(combined_rotator);
	// Components attachments
	constrain->SetupAttachment(link_A);
	constrain->ConstraintActor1 = this;
	constrain->ConstraintActor2 = this;
	constrain->ComponentName1.ComponentName = link_A->GetFName();
	constrain->ComponentName2.ComponentName = link_B->GetFName();
	// Set physical properties
	float stiff_value = 1.0e10f;
	float ang_stiff_value = 1.0e20f;
	float dampi_value = 1.0e8f;
	constrain->ConstraintInstance.ProfileInstance.LinearLimit.Stiffness = stiff_value;
	constrain->ConstraintInstance.ProfileInstance.LinearLimit.Damping = dampi_value;
	constrain->ConstraintInstance.ProfileInstance.LinearLimit.bSoftConstraint = true;
	constrain->ConstraintInstance.ProfileInstance.ConeLimit.Stiffness = ang_stiff_value;
	constrain->ConstraintInstance.ProfileInstance.ConeLimit.Damping = dampi_value;
	constrain->ConstraintInstance.ProfileInstance.ConeLimit.bSoftConstraint = true;
	constrain->ConstraintInstance.ProfileInstance.ConeLimit.ContactDistance = 10;
	constrain->ConstraintInstance.ProfileInstance.TwistLimit.Stiffness = stiff_value;
	constrain->ConstraintInstance.ProfileInstance.TwistLimit.Damping = dampi_value;
	constrain->ConstraintInstance.ProfileInstance.TwistLimit.bSoftConstraint = true;
	constrain->ConstraintInstance.DisableProjection();
	constrain->ConstraintInstance.UpdateLinearLimit();
	constrain->ConstraintInstance.UpdateAngularLimit();
	// constrain contrain
	constrain->SetMobility(EComponentMobility::Movable);
	constrain->SetLinearXLimit(ELinearConstraintMotion::LCM_Limited, 0.05f);
	constrain->SetLinearYLimit(ELinearConstraintMotion::LCM_Limited, 0.05f);
	constrain->SetLinearZLimit(ELinearConstraintMotion::LCM_Limited, 0.05f);
	constrain->SetAngularSwing1Limit(EAngularConstraintMotion::ACM_Limited, 0.1f);
	constrain->SetAngularSwing2Limit(EAngularConstraintMotion::ACM_Limited, 0.1f);
	constrain->SetAngularTwistLimit (EAngularConstraintMotion::ACM_Free, 180.0f);
	// end of setup
	return true;
}

bool ARobotMain::joint_setup_motor(uint16 joint_ID) // implementar
{
	if (!Joints_list.Contains(joint_ID)) {
		UE_LOG(LogTemp, Error, TEXT("Unable to find joint ID to setup motor."));
		return false; }
	FRobotJoints* joint_data = Joints_list.Find(joint_ID);
	if (joint_data == nullptr) {
		UE_LOG(LogTemp, Error, TEXT("Unable to find joint ID to setup motor."));
		return false; }
		UPhysicsConstraintComponent* constrain = joint_data->joint;
	if (constrain == nullptr) {
		UE_LOG(LogTemp, Error, TEXT("Unable to find joint ID to setup motor."));
		return false; }
	constrain->SetAngularDriveMode(EAngularDriveMode::TwistAndSwing);
	constrain->SetAngularDriveParams(10000000.0f, 1000.0f, 100000000.0f);
	constrain->ConstraintInstance.SetOrientationDriveTwistAndSwing(false, false);
	constrain->ConstraintInstance.SetAngularVelocityDriveTwistAndSwing(false, false);

	return true;
}

void ARobotMain::create_mesh_dictionary(const TArray<FString>& mesh_paths)
{
	for (const FString& path : mesh_paths)
	{
		ConstructorHelpers::FObjectFinder<UStaticMesh> MeshAsset(*path);
		if (MeshAsset.Succeeded()) {
			UStaticMesh* mesh = MeshAsset.Object;
			Models_list.Add(path, mesh);
		} else {
			UE_LOG(LogTemp, Warning, TEXT("Failed to load mesh at path: %s. Adding default sphere mesh."), *path);
			ConstructorHelpers::FObjectFinder<UStaticMesh> default_mesh_asset(TEXT("/Engine/BasicShapes/Sphere"));
			if (default_mesh_asset.Succeeded()) {
				UStaticMesh* default_mesh = default_mesh_asset.Object;
				Models_list.Add(path, default_mesh);
			} else {
				UE_LOG(LogTemp, Error, TEXT("Failed to load default sphere mesh."));
			}
		}
	}
}

void ARobotMain::setup_socket()
{
	if (SocketSubComp != nullptr){
		SocketSubComp->Socket_connect_to_server();
		// GetWorldTimerManager().SetTimer(timer_call_handler, this, &ARobotMain::python_call_handler, 0.02f, true);
	}
}

// Alvos de posição e velocidade devem ser atualizados na frame do parent
void ARobotMain::python_call_handler()
{
	uint8 messagetype = SocketSubComp->listen(); // tester remover retorno para analizar bug de violação
	if (messagetype == 255){ return; }
	switch (messagetype) {
		case 0: { // Null message type
			UE_LOG(LogTemp, Error, TEXT("Recieved message has an error or message type was declared 0."));
			break;
		}
		case 1: { // string log message type
			FString string_recived = SocketSubComp->get_string_from_inbuffer();
			UE_LOG(LogTemp, Warning, TEXT("String got: %s"), *string_recived);
			break;
		}
		case 2: { // calling for actuator's sensor data
			uint8 actuator_index = SocketSubComp->get_uint8_from_inbuffer();
			// select actuator
			if (!Joints_list.Contains(actuator_index)) {
				UE_LOG(LogTemp, Error, TEXT("Unable to find joint ID to setup."));
				break;}
			FRobotJoints* joint_data =  Joints_list.Find(actuator_index);
			if (joint_data == nullptr) {
				UE_LOG(LogTemp, Error, TEXT("Unable to find actuator ID: %u"), actuator_index);
				break;}
			UPhysicsConstraintComponent* Constrain = joint_data->joint;
			if (Constrain == nullptr) {
				UE_LOG(LogTemp, Error, TEXT("Unable to find actuator ID: %u"), actuator_index);
				break;}
			// define callback values
			float position = Constrain->ConstraintInstance.GetCurrentTwist();
			position = (position/PI)*180;
			float time_stamp = GetWorld()->GetRealTimeSeconds();
			// write callback and send.
			SocketSubComp->set_messagetype_value(12);
			SocketSubComp->append_unit8_to_outbuffer(actuator_index);
			SocketSubComp->append_float_to_outbuffer(position);
			SocketSubComp->append_float_to_outbuffer(time_stamp);
			SocketSubComp->send_outbuffer_data();
			break;
		}
		case 5: { // set angle target orientation
			// get parameters
			uint8 actuator_index = SocketSubComp->get_uint8_from_inbuffer();
			float position_value = SocketSubComp->get_float_from_inbuffer();
			// select actuator
			if (!Joints_list.Contains(actuator_index)) {
				UE_LOG(LogTemp, Error, TEXT("Unable to find joint ID to setup."));
				break;}
			FRobotJoints* joint_data =  Joints_list.Find(actuator_index);
			if (joint_data == nullptr) {
				UE_LOG(LogTemp, Error, TEXT("Unable to find actuator ID: %u"), actuator_index);
				break;}
			UPhysicsConstraintComponent* Constrain = joint_data->joint;
			if (Constrain == nullptr) {
				UE_LOG(LogTemp, Error, TEXT("Unable to find actuator ID: %u"), actuator_index);
				break;}
			// call order in the actuator
			position_value = (position_value/360)*PI*2;
			FQuat orientation =  FQuat(FVector(1.0f, 0.0f, 0.0f), position_value);
			Constrain->ConstraintInstance.SetAngularOrientationTarget(orientation);
			Constrain->ConstraintInstance.SetOrientationDriveTwistAndSwing(true, false);
			Constrain->ConstraintInstance.SetAngularVelocityDriveTwistAndSwing(false, false);
			// joint_data->link_base->GetBodyInstance()->WakeInstance();
			// joint_data->link_reac->GetBodyInstance()->WakeInstance();
			// define callback values
			float position = Constrain->ConstraintInstance.GetCurrentTwist();
			position = (position/PI)*180;
			float time_stamp = GetWorld()->GetRealTimeSeconds();
			// write callback and send.
			// UE_LOG(LogTemp, Display, TEXT("position sent: %f"), position);
			SocketSubComp->set_messagetype_value(15);
			SocketSubComp->append_unit8_to_outbuffer(actuator_index);
			SocketSubComp->append_float_to_outbuffer(position);
			SocketSubComp->append_float_to_outbuffer(time_stamp);
			SocketSubComp->send_outbuffer_data();
			break;
		}
		case 6: { // set angle target orientation
			// get parameters
			uint8 actuator_index = SocketSubComp->get_uint8_from_inbuffer();
			float velocity_value = SocketSubComp->get_float_from_inbuffer();
			// select actuator
			if (!Joints_list.Contains(actuator_index)) {
				UE_LOG(LogTemp, Error, TEXT("Unable to find joint ID to setup."));
				break;}
			FRobotJoints* joint_data =  Joints_list.Find(actuator_index);
			if (joint_data == nullptr) {
				UE_LOG(LogTemp, Error, TEXT("Unable to find actuator ID: %u"), actuator_index);
				break;}
			UPhysicsConstraintComponent* Constrain = joint_data->joint;
			if (Constrain == nullptr) {
				UE_LOG(LogTemp, Error, TEXT("Unable to find actuator ID: %u"), actuator_index);
				break;}
			// call order in the actuator
			// FRotator parent_transform = joint_data->link_base->GetComponentRotation();
			FVector relative_velocity = FVector(velocity_value, 0.0f, 0.0f);
			// FVector absolute_velocity = parent_transform.RotateVector(relative_velocity);
			Constrain->ConstraintInstance.SetAngularVelocityTarget(relative_velocity);
			Constrain->ConstraintInstance.SetOrientationDriveTwistAndSwing(false, false);
			Constrain->ConstraintInstance.SetAngularVelocityDriveTwistAndSwing(true, false);
			// define callback values
			float position = Constrain->ConstraintInstance.GetCurrentTwist();
			position = (position/PI)*180;
			float time_stamp = GetWorld()->GetRealTimeSeconds();
			// write callback and send.
			SocketSubComp->set_messagetype_value(16);
			SocketSubComp->append_unit8_to_outbuffer(actuator_index);
			SocketSubComp->append_float_to_outbuffer(position);
			SocketSubComp->append_float_to_outbuffer(time_stamp);
			SocketSubComp->send_outbuffer_data();
			break;
		}
		case 9: { // tester message type
			// recieving a call
			float float_recieved_1 = SocketSubComp->get_float_from_inbuffer();
			UE_LOG(LogTemp, Display, TEXT("float recieved: %f"), float_recieved_1);
			uint8 uint8_recieved = SocketSubComp->get_uint8_from_inbuffer();
			UE_LOG(LogTemp, Display, TEXT("uint8 recieved: %u"), uint8_recieved);
			FString string_recived = SocketSubComp->get_string_from_inbuffer();
			UE_LOG(LogTemp, Display, TEXT("String recieved: %s"), *string_recived);
			float float_recieved_2 = SocketSubComp->get_float_from_inbuffer();
			UE_LOG(LogTemp, Display, TEXT("float recieved: %f"), float_recieved_2);
			UE_LOG(LogTemp, Display, TEXT("Outside boundaries testing... trying to get a uint8 that do not fit in remainning message size"));
			uint8 uint8_recieved_2 = SocketSubComp->get_uint8_from_inbuffer();
			UE_LOG(LogTemp, Display, TEXT("uint8 recieved: %u"), uint8_recieved_2);
			// handling callback
			SocketSubComp->set_messagetype_value(19);
			SocketSubComp->append_float_to_outbuffer(3.1418f);
			const char* string_data = "This is a string sent as Callback from UE.";
			SocketSubComp->append_string_to_outbuffer(string_data);
			SocketSubComp->append_float_to_outbuffer(6.28000f);
			SocketSubComp->send_outbuffer_data();
			break;
		}
	}
}

