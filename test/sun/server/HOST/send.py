import socket
import time


# A로부터 데이터를 받습니다.


# 소켓 생성



#HOST='165.229.185.195'
HOST='192.168.50.71'
PORT =65432
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST,PORT))

HOST_2='192.168.232.134'
PORT_2=65433
sock_2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    data,addr=sock.recvfrom(1024)
    print("수신한 데이터",data.decode(),'from',addr)
    sock_2.sendto(data,(HOST_2,PORT_2))
    time.sleep(0.1)





