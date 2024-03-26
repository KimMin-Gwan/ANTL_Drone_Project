import socket
from socket import socket as Sock
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import time



class RealTimeAPI:
    def __init__(self):
        self.server_socket = None
        pass

    def __data_send(self, client_socket:Sock):
        try:
            while True:
                time.sleep(1)
                message = "hello world"
                client_socket.sendall(message.encode())
        except Exception as e:
            print(e)
        return
            
    def __data_recv(self, client_socket:Sock):
        try:
            while True:
                recv_data = client_socket.recv(1024)
                decode_data = recv_data.decode()
                print(']     >> Received From -> ', decode_data )
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





