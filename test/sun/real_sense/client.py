import socket
import cv2
import pyrealsense2 as rs
import numpy as np

UDP_IP = '165.229.185.195'
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Realsense pipeline 설정
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

# Realsense 카메라 시작
pipeline.start(config)

try:
    while True:
        # Realsense 프레임 읽기
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        
        # 프레임 데이터를 numpy 배열로 변환
        color_image = np.asanyarray(color_frame.get_data())

        # 프레임을 UDP 소켓으로 전송
        d = color_image.flatten()
        s = d.tostring()
        for i in range(20):
            sock.sendto(bytes([i]) + s[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

finally:
    # 리소스 해제
    pipeline.stop()
    cv2.destroyAllWindows()
    sock.close()
