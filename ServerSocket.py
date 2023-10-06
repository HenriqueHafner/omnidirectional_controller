import socket
import threading
import struct

#remover threading de server e adicionar ao tester de Server
class Server(threading.Thread): # the inheritance of threading.Thread is not mandatory, it is possible to use another implementation.
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.online_flag = True
        self.print_debug = False

    def run(self): #needs to me named run as a threading module requirements.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server set on {self.host}:{self.port}")
        try:
            client_socket, client_address = self.server_socket.accept()
            self.client_socket = client_socket
            self.client_socket.settimeout(2)
            self.client_address = client_address
            print("Client connected.")
        except Exception as e:
            print(f"Error while accepting connection: {e}")

    def call_HelloWorld_sring(self, message_str = "Hello World! called from python."):
        message_bytes = message_str.encode('utf-8')
        message_bytes += b'\x00'
        message_type = 1
        data = self.format_data_to_protocol(message_bytes, message_type)
        self.send_data_to_client(data)


    def format_data_to_protocol(self, data_bytes, message_type):
        """
        The protocol is composed by a header+data. the header has 3 bytes,
        first byte is a uint8 message_type, the fallowing 2 bytes are a uint16
        as data_size. . data_size is the
        expectated data size in bytes, corresponding to the data_bytes arg.

        Parameters
        ----------
        data_bytes : a sequence of bytes
        message_type : a uint8 like value
            message_type is used to indidicate to the other side
            what is data or what should be done with data

        Returns
        -------
        data : a sequence of bytes
            a copy of data_bytes with the protocol header.

        """
        type_bytes = struct.pack('<B', message_type)
        message_size = len(data_bytes)
        size_bytes = struct.pack('<H', message_size)
        data = type_bytes + size_bytes + data_bytes
        return data

    def incoming_data_handler(self):
        try:
            messageType_data = self.client_socket.recv(1)
            messageType = int.from_bytes(messageType_data, byteorder='little', signed=False)
            messageSize_data = self.client_socket.recv(2)
            messageSize = int.from_bytes(messageSize_data, byteorder='little', signed=False)    
            messageData = self.client_socket.recv(messageSize)
            if self.print_debug:
                print("Recieved:")
                self.print_bytes(messageType_data+messageSize_data+messageData)  
            return messageType, messageData
        except Exception as e:
            print("Error sending data to the client:", e)      
        return None, None

    def send_data_to_client(self, data):
        try:
            self.client_socket.sendall(data)
        except Exception as e:
            print("Error sending data to the client:", e)
        if self.print_debug:
            print("Sent:")
            self.print_bytes(data)

    def print_bytes(self, data):
        message_type = data[0:1]
        message_size = data[1:3]
        header_hex = " ".join(f"{byte:02X}" for byte in message_type + message_size)
        data_hex = " ".join(f"{byte:02X}" for byte in data[3:])
        total_bytes = len(data)
        print("Bytes:", header_hex, data_hex)
        print("Size:", total_bytes)

# robotics specifics implementation

    def send_type_1_message(self, message_str):
        message_bytes = message_str.encode('utf-8')
        data = self.format_data_to_protocol(message_bytes, 1)
        self.send_data_to_client(data)

    def send_type_2_message(self, actuator_index):
        actuator_index_bytes = struct.pack('<B', actuator_index)
        message_bytes = actuator_index_bytes
        data_to_send = self.format_data_to_protocol(message_bytes, 2)
        self.send_data_to_client(data_to_send)
        message_type_recieved, data_callback = self.incoming_data_handler()
        if message_type_recieved == 12:    
            return self.sensor_callback(actuator_index, data_callback)
        else:
            print("wrong message type in callback")
            return None, None

    # def send_type_4_message(self, actuator_index, torque_value, time_period_value):
    #     # values for call order
    #     message_type = 4
    #     actuator_index_bytes = struct.pack('<B', actuator_index)
    #     torque_bytes = struct.pack('<f', float(torque_value))
    #     time_period_bytes = struct.pack('<f', float(time_period_value))
    #     # message setup
    #     message_bytes = actuator_index_bytes + torque_bytes + time_period_bytes
    #     data_to_send = self.format_data_to_protocol(message_bytes, message_type)
    #     self.send_data_to_client(data_to_send)
    #     # handle callback
    #     message_type_recieved, data_callback = self.incoming_data_handler()
    #     if message_type_recieved == 14:    
    #         return self.sensor_callback(actuator_index, data_callback)
    #     else:
    #         print("wrong message type in callback")
    #         return None, None

    def send_type_5_message(self, actuator_index, position_value):
        # values for call order
        message_type = 5
        actuator_index_bytes = struct.pack('<B', int(actuator_index))
        position_bytes = struct.pack('<f', float(position_value))
        # message setup
        message_bytes = actuator_index_bytes + position_bytes
        data_to_send = self.format_data_to_protocol(message_bytes, message_type)
        self.send_data_to_client(data_to_send)
        # handle callback
        message_type_recieved, data_callback = self.incoming_data_handler()
        if message_type_recieved == 15:    
            return self.sensor_callback(actuator_index, data_callback)
        else:
            print("wrong message type in callback")
            return None, None
        return True

    def send_type_6_message(self, actuator_index, velocity_value):
        # values for call order
        message_type = 6
        actuator_index_bytes = struct.pack('<B', int(actuator_index))
        velocity_bytes = struct.pack('<f', float(velocity_value))
        # message setup
        message_bytes = actuator_index_bytes + velocity_bytes
        data_to_send = self.format_data_to_protocol(message_bytes, message_type)
        self.send_data_to_client(data_to_send)
        # handle callback
        message_type_recieved, data_callback = self.incoming_data_handler()
        if message_type_recieved == 16:    
            return self.sensor_callback(actuator_index, data_callback)
        else:
            print("wrong message type in callback")
            return None, None
        return True

    def bytes_to_string(self, byte_array, start_index):
        end_index = byte_array.find(0, start_index)
        if end_index != -1:
            byte_slice = byte_array[start_index:end_index]
            string_value = struct.unpack_from(str(len(byte_slice)) + 's', bytes(byte_slice))[0].decode('utf-8', 'ignore')
            return string_value, end_index+1
        return None

    def send_type_9_message(self): # message for testing
        #message defining
        message_type = 9
        float_1_bytes = struct.pack('<f', 3.1418)
        uint8_bytes = struct.pack('<B', 200)
        string_chars = "Text exchange testing"
        string_bytes = string_chars.encode('utf-8')
        string_bytes += b'\x00'
        float_2_bytes = struct.pack('<f', -3.1418)
        message_bytes = float_1_bytes + uint8_bytes + string_bytes + float_2_bytes
        formated_message_bytes = self.format_data_to_protocol(message_bytes, message_type)
        # send message
        self.send_data_to_client(formated_message_bytes)
        # callback
        message_type_recieved, data = self.incoming_data_handler()
        # interpreting bytes
        float_1_callback = struct.unpack_from('<f', data, 0)[0]
        string_callback, string_end_index = self.bytes_to_string(data, 4)
        float_2_callback = struct.unpack_from('<f', data, string_end_index)[0]
        # debug
        if self.print_debug:
            print("String recieved:", string_callback)
            print("Float 1: ", float_1_callback, "Float 2: ", float_2_callback)

    def sensor_callback(self, index_callback, data):
        if len(data) < 9:
            print("sensor callback data error, data is incomplete")
            return False
        actuator_index = struct.unpack_from('<B', data, 0)[0]
        if not (actuator_index == index_callback):
            print("Sensor Index and actuator index, callback mismatch.")
            return None, None
        actuator_position = struct.unpack_from('<f', data, 1)[0]
        actuator_sensor_timestamp = struct.unpack_from('<f', data, 5)[0]
        if self.print_debug:
            print(actuator_index, actuator_position,actuator_sensor_timestamp)
        return actuator_sensor_timestamp, actuator_position


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12300
    server_instance = Server(HOST, PORT)
    server_instance.start()

def end():
    server_instance.server_socket.close()
