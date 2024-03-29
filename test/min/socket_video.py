# 필요한 패키지 import
import socket # 소켓 프로그래밍에 필요한 API를 제공하는 모듈
import struct # 바이트(bytes) 형식의 데이터 처리 모듈
import pickle # 객체의 직렬화 및 역직렬화 지원 모듈
import cv2 # OpenCV(실시간 이미지 프로세싱) 모듈

# 서버 ip 주소 및 port 번호
ip = '192.168.1.3'
port = 50001

# 소켓 객체 생성
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 소켓 주소 정보 할당
server_socket.bind((ip, port))

# 연결 리스닝(동시 접속) 수 설정
server_socket.listen(10) 

print('클라이언트 연결 대기')

# 연결 수락(클라이언트 (소켓, 주소 정보) 반환)
client_socket, address = server_socket.accept()
print('클라이언트 ip 주소 :', address[0])


data_buffer = b""
data_size = struct.calcsize("L")  # unsigned long

while True:
    while len(data_buffer) < data_size:
        data_buffer += client_socket.recv(4096)

    packed_data_size = data_buffer[:data_size]
    data_buffer = data_buffer[data_size:]

    frame_size = struct.unpack(">L", packed_data_size)[0]

    while len(data_buffer) < frame_size:
        data_buffer += client_socket.recv(4096)

    frame_data = data_buffer[:frame_size]
    data_buffer = data_buffer[frame_size:]

    print(f"frame size : {frame_size} bytes")

    frame = pickle.loads(frame_data)    
    
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)


    







# 필요한 패키지 import
import cv2 # OpenCV(실시간 이미지 프로세싱) 모듈
import socket # 소켓 프로그래밍에 필요한 API를 제공하는 모듈
import pickle # 객체의 직렬화 및 역직렬화 지원 모듈
import struct # 바이트(bytes) 형식의 데이터 처리 모듈

# 서버 ip 주소 및 port 번호
ip = '192.168.1.3'
port = 50001

# 카메라 또는 동영상
capture = cv2.VideoCapture(0)

# 프레임 크기 지정
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # 가로
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # 세로


# 소켓 객체 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # 서버와 연결
    client_socket.connect((ip, port))
    
    print("연결 성공")
    
    # 메시지 수신
    while True:
        # 프레임 읽기
        retval, frame = capture.read()
        
        retval, frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        
        frame = pickle.dumps(frame)

        print("전송 프레임 크기 : {} bytes".format(len(frame)))
        client_socket.sendall(struct.pack(">L", len(frame)) + frame)

# 메모리를 해제
capture.release()


