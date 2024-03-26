import spidev
import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
CE_PIN = 25  # CE 핀은 GPIO 25번에 연결

# SPI 인터페이스 설정
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0.0 사용 (GPIO 8: CE0, GPIO 7: CE1)
spi.max_speed_hz = 1000000  # SPI 통신 속도 설정 (1MHz)

# nRF24L01 레지스터 명령어 정의
R_REGISTER = 0x00
FLUSH_RX = 0xE2
NOP = 0xFF

# nRF24L01 레지스터 주소 정의
RX_ADDR_P0 = 0x0A
RX_PW_P0 = 0x11
CONFIG = 0x00
STATUS = 0x07

# nRF24L01 설정 값 정의
CONFIG_VAL = 0b00001011  # PRIM_RX 비트를 1로 설정하여 RX 모드로 설정

# 함수: 레지스터 쓰기
def write_register(address, data):
    spi.xfer([address | 0b00100000, data])

# 함수: 레지스터 읽기
def read_register(address):
    return spi.xfer([address & 0b00011111, NOP])[1:]

# 함수: 초기화 및 설정
def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CE_PIN, GPIO.OUT)
    GPIO.output(CE_PIN, GPIO.LOW)

    # RX 주소 설정 (주소는 송신 모듈의 TX 주소와 동일해야 함)
    rx_address = [0x12, 0x34, 0x56, 0x78, 0x90]
    for i, addr in enumerate(rx_address):
        write_register(RX_ADDR_P0 + i, addr)

    # Payload 길이 설정
    write_register(RX_PW_P0, len("hello world"))

    # nRF24L01 설정
    write_register(CONFIG, CONFIG_VAL)

# 함수: 데이터 수신
def receive_data():
    # CE 핀 활성화
    GPIO.output(CE_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # 10us 지연 필요

    # 데이터 수신 대기
    while True:
        status = read_register(STATUS)
        if status[0] & 0b01000000:
            # 데이터 수신 완료
            received_data = spi.xfer([R_REGISTER | 0x61] + [NOP] * len("hello world"))
            break

    # CE 핀 비활성화
    GPIO.output(CE_PIN, GPIO.LOW)

    return "".join(chr(byte) for byte in received_data[1:])

# 메인 함수
def main():
    try:
        initialize()
        while True:
            # 데이터 수신
            received_data = receive_data()
            print("Data received:", received_data)
            time.sleep(1)  # 1초 대기 후 다음 데이터 수신

    except KeyboardInterrupt:
        spi.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()