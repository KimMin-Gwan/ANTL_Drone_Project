## 외부 통신을 위한 view


# 서버로 부터 Key를 받고
# 서버한테 비디오 보내기


import socket
from socket import socket as Sock
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import struct
import pickle

class RealTimeAPI:
    def __init__(self,):
        self.__client_socket = None

    def __video_send(self, controller):
        try:
            while True:
                inputdata = input(">> input : ")
                frame = controller.get_video_frame()
                frame = pickle.dumps(frame)
                self.__client_socket.sendall(
                    struct.pack(">L", len(frame)) + frame)
        except Exception as e:
            print("connection error(send)")
            print(e)
        return


    def __key_recv(self, controller):
        # 연결 초기 설정 하고 들어와야댐
        try:
            while True:
                recv_data = self.__client_socket.recv(1024)
                decoded_data = recv_data.decode() # decode
                s_data = decoded_data.split(" ", 4) #head analyze
                if s_data[0] != "k":
                    print("This is Not key")
                    print(">>> ", s_data)
                    continue
                controller.set_control_key(s_data[1:5])

        except Exception as e:
            print("connection error(recv)")
            print(e)
        return
    
    # 핸들링
    def __rt_connect_handler(self, controller):
        send_thread = Thread(target=self.__video_send,
                        args=(controller,))
        recv_thread = Thread(target=self.__key_recv, 
                        args=(controller,))

        send_thread.start()
        recv_thread.start()

    # 자식스레드가 나옴 (필요하면 부모에서 돌려야함)
    def try_connect(self, controller, host, port):
        self.__client_socket = Sock(AF_INET, SOCK_STREAM)
        self.__client_socket.connect((host, port))
        connection = Thread(self.__rt_connect_handler,
                            args=(controller,))
        connection.start()  # 아니 부모 어디감?


