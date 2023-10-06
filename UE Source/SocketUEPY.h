// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Networking.h"
// #include "RobotMain.h"
#include "SocketUEPY.generated.h"


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class BOXBOT_API USocketUEPY : public UActorComponent
{
	GENERATED_BODY()
public:	
	USocketUEPY();
protected:
	virtual void BeginPlay() override;

/*
 ### Protocol for message exchange, in standart setup ###
 message in bytes : [Header + Data]
 Header : 3 bytes: uint8(1byte) + uint16(2bytes):
 Header meaning : message type uint8(1byte); data size uint16(2bytes)
 Example:
 [header ] [data                                ] [garbage in buffer  ]
 [01 00 0D 48 65 6C 6C 6F 20 57 6F 72 6C 64 21 00 FF A2 A1 A0 00 00 00]
  ^^;^^ ^^;^^                                  ^^;^^ ^^ ^^ ^^ ^^ ^^ ^^
  || || ||;|| || || || || || || || || || || || ||;|| || || || || || || 
  || || ||;|| || || || || || || || || || || || ||:FF A2 A1 A0 00 00 00: garbage data left in buffer, ignored to compose a message data.
  || || ||;|| || || || || || || || || || || || || 
  || || ||;48 65 6C 6C 6F 20 57 6F 72 6C 64 21 00:
  || || ||  [Data bytes with size MessageSize as defined in header MessageSize bytes-
  || || ||   in this example, data is a string of char: "Hello World!" plus the end -
  || || ||   null char 00, with total size = 13 bytes]
  || || ||
  || 00 0D: uint16 MessageSize = 00 0D = 13
  ||
  01:MessageType uint8

  cursor_pos is a array index available to writes a byte.
*/


// Methods
public:
	void Socket_attributes_initialization();
	bool Socket_connect_to_server();
	void Socket_destroy();
	uint8 listen();
	void send_outbuffer_data();
	void set_messagetype_value(uint8 messagetype_value);
	void append_float_to_outbuffer	(float value);
	void append_unit8_to_outbuffer	(uint8 value);
	void append_string_to_outbuffer(const char* string_first_char_ptr);
	uint8 get_uint8_from_inbuffer();
	float get_float_from_inbuffer();
	FString get_string_from_inbuffer();
	void log_bytes(const TArray<uint8>& bytes_array, uint16 index_start = 0, uint16 index_end = 0);
	void log_input_buffer();
	void log_output_buffer();
protected:
	bool parse_input_header_params();
	void set_messagetype_to_outbuffer();
	void set_data_size_to_outbuffer();

// Attributes
public: 
	FSocket* Socket = nullptr;
	UPROPERTY(VisibleAnywhere)
	FString ServerIP = TEXT("127.0.0.1");
    UPROPERTY(VisibleAnywhere)
	int32 ServerPort = 12300;
	bool is_connected = false;
	UPROPERTY(EditAnywhere)
	int16 debug_value_uint16 = 0;
	UPROPERTY(EditAnywhere)
	int16 debug_value_float = 0.0f;
	bool should_print_cases = false;

protected:
	uint8 protocol_header_size = sizeof(uint8) + sizeof(uint16); // number of byter for header, input and output
	uint16 buffer_size_for_data = 512; // number of bytes for data, input and output
	uint16 interface_buffer_size = buffer_size_for_data + protocol_header_size; // maximum number of bytes in a socket message.
	TArray<uint8> output_bytes_buffer;
	TArray<uint8> input_bytes_buffer;
	uint32 data_available_read;
	uint8 null_message_type = 0;
	uint8  output_MessageType;
	uint16 output_data_size;
	uint8   input_MessageType;
	uint16  input_data_size;
	uint16 output_cursor_pos = protocol_header_size; // data cursor scope, initialized after header end position
	uint16  input_cursor_pos = protocol_header_size; // data cursor scope, initialized after header end position
	uint16 input_data_last_byte_index;

};
