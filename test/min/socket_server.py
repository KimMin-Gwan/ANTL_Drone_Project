import socket
from socket import socket as Sock
from threading import Thread
import time

HOST = "127.0.0.1"
PORT = 5000

def data_send(client_socket:Sock):
    try:
        while True:
            time.sleep(1)
            message = "hello world"
            client_socket.sendall(message.encode())
    except Exception as e:
        print(e)
    return
        
def data_recv(client_socket:Sock):
    try:
        while True:
            recv_data = client_socket.recv(1024)
            decode_data = recv_data.decode()

            print(']     >> Received From -> ', decode_data )

    except Exception as e:
        print(e)
    return

def handle_client(client_socket:Sock):
    send_thread = Thread(target=data_send, args=(client_socket,))
    recv_thread = Thread(target=data_recv, args=(client_socket,))
    send_thread.start()
    recv_thread.start()

def waiting_client(server_socket:Sock):
    try:
        print("Real-time send system lunching")
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"client accepted : {client_address}")
            if client_socket:
                client_thread = Thread(target=handle_client, args=(client_socket,))
                client_thread.start()

    except Exception as e:
        print(e)

def socket_start():
    server_socket = Sock(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[:  Started server process ")
    print(f"[:  Waiting for application startup. ")
    print(f"[:  WSGI running on [http://{HOST}:{str(PORT)} (Press CTRL+C to quit)] ")

    rt_thread = Thread(target=waiting_client, args=(server_socket,))
    rt_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        rt_thread.join()
        print(f"[:  Shutting down. ")
        print(f"[:  Finished  server process. ")


        
if __name__ == "__main__":
    socket_start()

