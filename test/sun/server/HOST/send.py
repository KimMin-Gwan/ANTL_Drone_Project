import socket
import time
import sys

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
    str_2=data.decode()+"\n"
    if(len(str_2)!=21):
        print("h\n")
    sock_2.sendto(data,(HOST_2,PORT_2))





