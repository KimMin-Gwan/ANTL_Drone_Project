
# 필요한 패키지 import
import socket # 소켓 프로그래밍에 필요한 API를 제공하는 모듈
import struct # 바이트(bytes) 형식의 데이터 처리 모듈
import pickle # 객체의 직렬화 및 역직렬화 지원 모듈
import cv2 # OpenCV(실시간 이미지 프로세싱) 모듈
import numpy

# 서버 ip 주소 및 port 번호
ip = '192.168.14.130'
port = 5001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

s = [b'\xff' * 46080 for x in range(20)]     # 640*480*3 을 총 20개로 나눠서 보냄 udp 최대 용량때문에 

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

while True:
    picture = b''

    data, addr = sock.recvfrom(46081)
    s[data[0]] = data[1:46081]
    if data[0] == 19:  #맨마지막 flag오면 
        for i in range(20):
            picture += s[i]  #다합쳐

        frame = numpy.fromstring(picture, dtype=numpy.uint8)
        frame = frame.reshape(480, 640, 3)
        cv2.imshow("frame", frame)
        out.write(frame)

        #message = "hello_client"
        #sock.sendto(message.encode(), addr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            sock.close()
            break
    

# # 소켓 객체 생성
# server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# # 소켓 주소 정보 할당
# server_socket.bind((ip, port))

# # 연결 리스닝(동시 접속) 수 설정
# server_socket.listen(10) 

# print('클라이언트 연결 대기')

# # 연결 수락(클라이언트 (소켓, 주소 정보) 반환)
# client_socket, address = server_socket.accept()
# print('클라이언트 ip 주소 :', address[0])


# data_buffer = b""
# data_size = struct.calcsize("L")  # unsigned long

# while True:
#     while len(data_buffer) < data_size:
#         data_buffer += client_socket.recv(4096)

#     packed_data_size = data_buffer[:data_size]
#     data_buffer = data_buffer[data_size:]

#     frame_size = struct.unpack(">L", packed_data_size)[0]

#     while len(data_buffer) < frame_size:
#         data_buffer += client_socket.recv(4096)

#     frame_data = data_buffer[:frame_size]
#     data_buffer = data_buffer[frame_size:]

#     print(f"frame size : {frame_size} bytes")

#     frame = pickle.loads(frame_data)    
    
#     frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

#     cv2.imshow('frame',frame)	# 이미지 보여주기
    
#     key = cv2.waitKey(25)
#     if key == 27:
#         break

