import socket
import time
import sys

# A로부터 데이터를 받습니다.


# 소켓 생성



HOST='127.0.0.1'
server_port=5001
#HOST='192.168.50.71'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,server_port))
sock.listen(1)




sock.bind((HOST,PORT))

HOST_2='192.168.232.136'
PORT_2=65433
sock_2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    data,addr=sock.recvfrom(1024)
    sock_2.sendto(data,(HOST_2,PORT_2))





