
# 소켓 생성


import socket

HOST='192.168.232.134'
PORT =65432
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST,PORT))
while True:
    data,addr=sock.recvfrom(1024)
    
    print("수신한 데이터",data.decode(),'from',addr)


        