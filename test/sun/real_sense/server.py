import socket
import numpy as np
import cv2

UDP_IP = "165.229.185.195"
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# OpenCV 윈도우 생성
#cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('Video', 640, 480)

while True:
    picture = b''

    # 데이터 수신
    for _ in range(20):
        data, addr = sock.recvfrom(46080)  # 각 프레임은 46080바이트 크기
        print(data)
        picture += data

    # 수신한 데이터를 NumPy 배열로 변환하여 영상으로 표시
    frame = np.frombuffer(picture, dtype=np.uint8)
    frame = frame.reshape(480, 640, 3)  # 이미지 크기에 맞게 재구성
    cv2.imshow("Video", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 윈도우 닫기 및 소켓 종료
cv2.destroyAllWindows()
sock.close()
