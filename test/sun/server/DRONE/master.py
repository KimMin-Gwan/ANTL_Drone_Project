
# 소켓 생성


import socket
import re
#HOST='165.229.185.195'

HOST='192.168.232.134'

#HOST='10.10.88.97'
PORT =65433
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST,PORT))
while True:
    data,addr=sock.recvfrom(1024)
    my_data=(data.decode().split(":"))
    roll=(float(my_data[0])-500)
    throttle=(float(my_data[1])/1500.0)
    yaw=(float(my_data[2])-500)
    pitch=float(my_data[3])-500
# 추출된 숫자를 범위 내에 조정하여 변수에 저장합니다.

    print("수신한 데이터",roll,throttle,yaw,pitch)


        