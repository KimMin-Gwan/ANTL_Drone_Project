from socket import *
from socket import socket as Sock
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import struct
import pickle


class RealTimeAPI:
    def __init__(self):
        self.server_socket = None
        self.data_buffer = b""
        self.video_buffer_size = struct.calcsize("L") # unsigned long
        self.data = [b'0 0 0 0 0']

    def __data_send(self, client_socket:Sock):
        print("recv start")
        try:
           while True:
                data = self.data[0]
                client_socket.sendall(data)

        except Exception as e:
            print("send died")
            print(e)
        return
            
    def __data_recv(self, client_socket:Sock):
        print("recv start")
        while True:
            try:
                recv_data = client_socket.recv(1024)

                self.data[0] = recv_data
            except Exception as e:
                print("recv died")
                print(e)

    def __handle_client(self, client_socket):
        try:
            send_thread = Thread(target=self.__data_send, args=(client_socket,))
            recv_thread = Thread(target=self.__data_recv, args=(client_socket,))
            send_thread.start()
            recv_thread.start()
        except:
            print("handle_client died")


    def waiting_client(self, server_socket:Sock):
        self.server_socket = server_socket
        try:
            print("Real-time send system lunching")
            client_socket, client_address = self.server_socket.accept()
            print(f">> Client {client_address} has connected")
            self.__handle_client(client_socket)

        except Exception as e:
            print("wait_client died")
            print(e)


class mingcorn:
    def run(app:RealTimeAPI, host:str="192.168.232.136", port:int=5001):
        server_socket = Sock(AF_INET, SOCK_STREAM)  
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[:  Started RT SERVER process ")
        print(f"[:  Waiting for RT_application startup. ")
        print(f"[:  WSGI running on [http://{host}:{str(port)}. ")

        rt_thread = Thread(target=app.waiting_client, args=(server_socket,))
        rt_thread.start()
        return


if __name__ == "__main__":
    app = RealTimeAPI()
    mingcorn.run(app=app)