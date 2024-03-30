from socket import *
from socket import socket as Sock
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import struct
import pickle


class RealTimeAPI:
    def __init__(self, controller):
        self.server_socket = None
        self.data_buffer = b""
        self.video_buffer_size = struct.calcsize("L") # unsigned long
        self.controller = controller

    def __data_send(self, client_socket:Sock):
        print("recv start")
        try:
           while True:
                frame = self.controller.get_video()
                frame = pickle.dumps(frame)
                client_socket.sendall(struct.pack(">L", len(frame)) + frame)

        except Exception as e:
            print(e)
        return
            
    def __data_recv(self, client_socket:Sock):
        print("recv start")
        try:
            while True:
                recv_data = client_socket.recv(1024)
                decoded_data = recv_data.decode()
                print(decoded_data)

                data = decoded_data.split(' ', 4)
                key_data = data[0:4]
                mode_data = data[4]

                self.controller.set_recv_data(key_data, mode_data)
                
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
            client_socket, client_address = self.server_socket.accept()
            print(f">> Client {client_address} has connected")
            self.__handle_client(client_socket)

        except Exception as e:
            print(e)


class mingcorn:
    def run(app:RealTimeAPI, host:str="127.0.0.1", port:int=5000):
        server_socket = Sock(AF_INET, SOCK_STREAM)  
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[:  Started RT SERVER process ")
        print(f"[:  Waiting for RT_application startup. ")
        print(f"[:  WSGI running on [http://{host}:{str(port)}. ")

        rt_thread = Thread(target=app.waiting_client, args=(server_socket,))

        return rt_thread


