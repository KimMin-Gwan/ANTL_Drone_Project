import socket
from socket import socket as Sock
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import time
import struct
import pickle

class RealTimeAPI:
    def __init__(self):
        self.server_socket = None
        self.data_buffer = b""
        self.video_buffer_size = struct.calcsize("L") # unsigned long
        self.get_route_map = {}
        self.post_route_map = {}

    def __data_send(self, client_socket:Sock):
        try:
            while True:
                send_data:str = self.__execute_function(route="/key_drone")
                encoded_data = send_data.encode()
                client_socket.sendall(encoded_data)
        except Exception as e:
            print(e)
        return
            
    def __data_recv(self, client_socket:Sock):
        try:
            while True:
                recv_data = client_socket.recv(1024)
                endpoint, head, body = self.__analyzer(recv_data)
                if head == b'v':
                    packed_data_size = body[:self.video_buffer_size]
                    frame_size = struct.unpack(">L", packed_data_size)[0]
                    self.data_buffer += body[self.video_buffer_size:]
                elif head == b'k':
                    data = body.decode()
                    self.__execute_function(route=endpoint,data=data)
                
                if len(self.data_buffer) > self.video_buffer_size:
                    frame_data = self.data_buffer[:frame_size]
                    self.data_buffer = self.data_buffer[frame_size:]
                    frame = pickle.loads(frame_data)
                    self.__execute_function(route=endpoint, data=frame)
        except Exception as e:
            print(e)
        return

    def __handle_client(self, client_socket):
        send_thread = Thread(target=self.__data_send, args=(client_socket,))
        recv_thread = Thread(target=self.__data_recv, args=(client_socket,))
        send_thread.start()
        recv_thread.start()

    def waiting_client(self, server_socket:Sock):
        self.server_socket = server_socket
        try:
            print("Real-time send system lunching")
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"client accepted : {client_address}")
                if client_socket:
                    client_thread = Thread(target=self.__handle_client, args=(client_socket,))
                    client_thread.start()

        except Exception as e:
            print(e)

    # "k data" "v data"
    def __analyzer(self, data:str):
        head, body_data = data.split(b' ', 1)

        if head == b"v":
            endpoint = "/video_recv"
        elif head == b"k":
            endpoint = "/key_apk"
        else:
            print("Invalid Head")
            print(f"[:  {head} | SERVER ERROR -> BAD HEADER")
            endpoint = "/error"
        return endpoint, head, body_data

    def get(self, route):
        def get_decorator(func):
            self.get_route_map[route] = func
            return func
        return get_decorator
    
    def post(self, route):
        def post_decorator(func):
            self.post_route_map[route] = func
            return func
        return post_decorator

    # route, data
    def __execute_function(self, route, data=None):
        if route in self.get_route_map:
            return self.get_route_map[route]()
        elif route in self.post_route_map:
            return self.post_route_map[route](data)
        else:
            print("Invalid Route")
            print(f"[:  {route} | SERVER ERROR -> BAD ENDPOINT ")

class mingcorn:
    def run(app:RealTimeAPI, host:str, port:int):
        server_socket = Sock(AF_INET, SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[:  Started RT SERVER process ")
        print(f"[:  Waiting for RT_application startup. ")
        print(f"[:  WSGI running on [http://{host}:{str(port)}. ")

        rt_thread = Thread(target=app.waiting_client, args=(server_socket,))
        rt_thread.start()

        return rt_thread





