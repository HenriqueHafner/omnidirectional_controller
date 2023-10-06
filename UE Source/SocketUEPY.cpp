#include "SocketUEPY.h"

USocketUEPY::USocketUEPY()
{
	PrimaryComponentTick.bCanEverTick = true;
	output_bytes_buffer.SetNumZeroed(interface_buffer_size);
    input_bytes_buffer.SetNumZeroed(interface_buffer_size);
}

void USocketUEPY::BeginPlay()
{
	Super::BeginPlay();
}

/// ####### Socket connection implementation #######

bool USocketUEPY::Socket_connect_to_server()
{
	if (Socket != nullptr) {
		UE_LOG(LogTemp, Warning, TEXT("Attempting to reach another socket server when a Socket object is already set.")); 
		return false; }
    TSharedPtr<FInternetAddr>  Address = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->CreateInternetAddr();
    bool bIsValid;
    Address->SetIp(*ServerIP, bIsValid);
    Address->SetPort(ServerPort);
    if (!bIsValid) {
		UE_LOG(LogTemp, Error, TEXT("Invalid IP address: %s"), *ServerIP);
		return false; }   
	Socket = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->CreateSocket(NAME_Stream, TEXT("default"), false);
	if (Socket) {
		if (Socket->Connect(*Address)) {
            is_connected = true;
			UE_LOG(LogTemp, Warning, TEXT("UE_Socket connected to server."));
			return true;
		} else {
            UE_LOG(LogTemp, Error, TEXT("Failed to connect to the server."));
			return false; }
    } else {
        UE_LOG(LogTemp, Error, TEXT("Failed to create socket.")); }
	return false;
}

void USocketUEPY::Socket_destroy()
{
        if (Socket != nullptr) {
			ESocketConnectionState connection_state;
			connection_state = Socket->GetConnectionState();
			if (connection_state == ESocketConnectionState::SCS_Connected) {
				Socket->Close();
				ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(Socket); }
		}
}

void USocketUEPY::log_bytes(const TArray<uint8>& bytes_array, uint16 index_start, uint16 index_end)
{
    if (index_start >= bytes_array.Num() || index_start > index_end)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid indices provided to log bytes."));
        return;
    }

    if (index_end == 0 || index_end >= bytes_array.Num())
    {
        index_end = bytes_array.Num() - 1;
    }

    FString string_of_hex;
    for (uint16 i = index_start; i <= index_end; ++i)
    {
        string_of_hex += FString::Printf(TEXT("%02X "), bytes_array[i]);
    }
    UE_LOG(LogTemp, Display, TEXT("Bytes: %s"), *string_of_hex);
}

void USocketUEPY::log_input_buffer()
{
    UE_LOG(LogTemp, Display, TEXT("Input buffer values until message size:"));
    log_bytes(input_bytes_buffer, 0, input_data_last_byte_index); //input_data_last_byte_index
}

void USocketUEPY::log_output_buffer()
{
    UE_LOG(LogTemp, Display, TEXT("Output buffer values until message size:"));
    log_bytes(output_bytes_buffer, 0, output_cursor_pos - 1);
}

/// ####### Input messages implementation #######

uint8 USocketUEPY::listen() { // checar getdata repetititvo
    if (Socket->HasPendingData(data_available_read)) { //reimplementar limpo
        if (data_available_read < protocol_header_size) {
            return null_message_type;
        }
    } else {
        return 255;
    }
    // Geting data from socket, the number of bytes to get is defined by the message size value got in the header.
    bool header_parsing_status = parse_input_header_params(); // sucess status of the header bytes interpretation from socket.
    if (!header_parsing_status) { return null_message_type; }
    uint8* buffer_first_byte_ptr = input_bytes_buffer.GetData();
    uint8* data_first_byte_ptr = buffer_first_byte_ptr + protocol_header_size;
    int32 message_bytes_read = 0;
    Socket->Recv(data_first_byte_ptr, input_data_size, message_bytes_read); // reading data bytes
    if (message_bytes_read != input_data_size) {
        UE_LOG(LogTemp, Error, TEXT("Received data size does not match expected message size."));
        return null_message_type; }
    input_cursor_pos = protocol_header_size; // cursor that aims to a availale index position in a byte array , initialized after header section
    input_data_last_byte_index = protocol_header_size + input_data_size - 1; // index for last data byte write in buffer.
    if (should_print_cases) { log_input_buffer(); }
    return input_MessageType;
}

bool USocketUEPY::parse_input_header_params() { // reads bytes from socket to compose a message header in the input_buffer.
    uint8* buffer_first_byte_ptr = input_bytes_buffer.GetData();
    int32  header_bytes_read = 0;
    Socket->Recv(buffer_first_byte_ptr, protocol_header_size, header_bytes_read);   // get header bytes for incomming message
    if (header_bytes_read != protocol_header_size) { return false; }
    FMemory::Memcpy((uint8*)&input_MessageType, buffer_first_byte_ptr, 1);  // copy MessageType value from buffer header
    FMemory::Memcpy((uint8*)&input_data_size, buffer_first_byte_ptr+sizeof(input_MessageType), 2);  // copy MessageSize value from buffer header
    if (should_print_cases) {
        UE_LOG(LogTemp, Display,TEXT("input_message_type %d"), input_MessageType);
        UE_LOG(LogTemp, Display,TEXT("input_data_size %d"), input_data_size); }
    if (input_data_size == 0) {
        UE_LOG(LogTemp, Error, TEXT("Data expected size was interpreted as 0."));
        return false; }
    if (input_data_size > buffer_size_for_data) {
        UE_LOG(LogTemp, Error, TEXT("Data expected size is too long, ignoring message."));
        return false; }
    return true;
}

uint8 USocketUEPY::get_uint8_from_inbuffer()
{
    uint16 cursor_shift = sizeof(uint8);
    if ( input_cursor_pos + cursor_shift - 1  > input_data_last_byte_index) {
        UE_LOG(LogTemp, Error, TEXT("Insuficient bytes after cursor position to interpret a uint8, returning 1"));
        return 1;
    }
    uint8* buffer_first_byte_ptr = input_bytes_buffer.GetData();
    uint8* converted_var_ptr = buffer_first_byte_ptr + input_cursor_pos;
    input_cursor_pos += cursor_shift;
    return *converted_var_ptr;
}

float USocketUEPY::get_float_from_inbuffer()
{
    uint16 cursor_shift = sizeof(float);
    if ( input_cursor_pos + cursor_shift - 1  > input_data_last_byte_index) {
        UE_LOG(LogTemp, Error, TEXT("Insuficient bytes after cursor position to interpret a float, returning 1.0f"));
        return 1.0f;
    }
    uint8* buffer_first_byte_ptr = input_bytes_buffer.GetData();
    uint8* float_first_byte_ptr  = buffer_first_byte_ptr + input_cursor_pos;
    float* converted_var_ptr = (float*) float_first_byte_ptr;
    input_cursor_pos += cursor_shift;
    return *converted_var_ptr;    
}

FString USocketUEPY::get_string_from_inbuffer()
{
    // Start from the current cursor position
    uint16 index_scope = input_cursor_pos;
    for (; index_scope <= input_data_last_byte_index; ++index_scope)
    {
        if (input_bytes_buffer[index_scope] == 0) // Found the null byte, update the cursor and return the string
        {
            uint8* buffer_first_byte_ptr = input_bytes_buffer.GetData();
            uint8* buffer_string_start_ptr = buffer_first_byte_ptr + input_cursor_pos; // offset pointer
            uint16 number_of_chars = index_scope - input_cursor_pos;
            FString ReceivedMessage = FString((const ANSICHAR*)buffer_string_start_ptr);
            input_cursor_pos = index_scope + 1;
            return ReceivedMessage;
        }
    }
    // If no null byte is found, return an empty string
    return FString();
}

/// ####### Output messages implementation #######

void USocketUEPY::append_unit8_to_outbuffer(uint8 value)
{
    uint8* memory_relative_position = output_bytes_buffer.GetData() + output_cursor_pos;
    *memory_relative_position = value;
    output_cursor_pos += 1;
}

void USocketUEPY::append_float_to_outbuffer(float value)
{
    uint8* memory_relative_position = output_bytes_buffer.GetData() + output_cursor_pos;
    FMemory::Memcpy(memory_relative_position, &value, 4);
    output_cursor_pos += 4;
}

void USocketUEPY::append_string_to_outbuffer(const char* string_first_char_ptr)
{
    uint16 string_size = strlen(string_first_char_ptr)+1; // size of string, adding 1 to also count the end byte 00
    if (output_cursor_pos + string_size <= output_bytes_buffer.Num()) {
        uint8* memory_relative_position = output_bytes_buffer.GetData() + output_cursor_pos;
        FMemory::Memcpy(memory_relative_position, string_first_char_ptr, string_size); // Copy the string to the output buffer
        output_cursor_pos += string_size; // Update the cursor position in the output buffer
    } else {
        // Handle the case where there is not enough space in the output buffer
        UE_LOG(LogTemp, Error, TEXT("Output buffer is not large enough to append the string.")); }
}


void USocketUEPY::send_outbuffer_data()
{
    int32 BytesSent = 0;
    uint8* buffer_first_byte_ptr = output_bytes_buffer.GetData();
    set_data_size_to_outbuffer();
    
    Socket->Send(buffer_first_byte_ptr, output_cursor_pos, BytesSent); // send all buffed bytes, header and data, until final writing cursor position
    if (should_print_cases) {
        log_output_buffer();
        UE_LOG(LogTemp, Display, TEXT("Number of bytes sent: %d"), BytesSent); }
    output_cursor_pos = protocol_header_size;
}

void USocketUEPY::set_messagetype_value(uint8 messagetype_value)
{
    output_MessageType = messagetype_value;
    set_messagetype_to_outbuffer();
}

void USocketUEPY::set_messagetype_to_outbuffer()
{
    uint8* buffer_first_byte_ptr = output_bytes_buffer.GetData();
    *buffer_first_byte_ptr = output_MessageType;   
}

void USocketUEPY::set_data_size_to_outbuffer()
{
    uint8* buffer_first_byte_ptr = output_bytes_buffer.GetData();
    // setting header bytes that represents messagesize.
    uint16 data_size = output_cursor_pos - protocol_header_size;
    FMemory::Memcpy(buffer_first_byte_ptr+1, &data_size, 2); // writing 2 bytes from a uint16 in position 1 and 2 of output_bytes_buffer
}
