import socket

# 서버 주소와 포트
#HOST = '165.229.185.195'
HOST = '10.10.88.97'
PORT = 65432
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg=input("->")
    sock.sendto(msg.encode(),(HOST,PORT))
