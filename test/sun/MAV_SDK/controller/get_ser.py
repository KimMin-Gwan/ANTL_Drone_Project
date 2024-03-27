import serial
import struct

# 시리얼 포트 설정
serial_port = '/dev/ttyAMA0'  # 라즈베리파이의 시리얼 포트에 따라 다를 수 있습니다.
baud_rate = 57600  # Pixhawk4와의 통신 속도에 따라 설정

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)

# RC 값 읽기
while True:
    # SBUS 프레임은 25바이트로 구성됩니다.
    # RC 채널 값은 16바이트에서 2바이트씩 끊어서 추출할 수 있습니다.
    rc_frame = ser.read(25)
    if len(rc_frame) == 25:
        # RC 채널 값 추출
        channels = struct.unpack('<HHHHHHHHHHHHHHHH', rc_frame[3:23])
        
        # 각 채널 값은 1000에서 2000 사이의 값으로 나타납니다.
        # 따라서 이 값을 적절한 범위로 변환하여 출력할 수 있습니다.
        pitch = channels[1]
        yaw = channels[2]
        roll = channels[0]
        
        print("Pitch:", pitch, "Yaw:", yaw, "Roll:", roll)

# 시리얼 포트 닫기
ser.close()
