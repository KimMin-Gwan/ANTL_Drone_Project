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
W_REGISTER = 0x20
FLUSH_TX = 0xE1
NOP = 0xFF

# nRF24L01 레지스터 주소 정의
TX_ADDR = 0x10

# 함수: 레지스터 쓰기
def write_register(address, data):
    spi.xfer([W_REGISTER | address, data])

# 함수: 초기화 및 설정
def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CE_PIN, GPIO.OUT)
    GPIO.output(CE_PIN, GPIO.LOW)

    # TX 주소 설정 (주소는 같은 그룹에 속해야 함)
    tx_address = [0x12, 0x34, 0x56, 0x78, 0x90]
    for i, addr in enumerate(tx_address):
        write_register(TX_ADDR + i, addr)

# 함수: 데이터 송신
def transmit_data(data):
    # 데이터 전송 전 CE 핀 활성화
    GPIO.output(CE_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # 10us 지연 필요

    # 데이터 송신
    spi.xfer([W_REGISTER | FLUSH_TX])  # TX FIFO 비우기
    spi.xfer([W_REGISTER | 0x00])  # W_TX_PAYLOAD 커맨드 전송
    spi.xfer(list(data.encode()))  # 데이터 전송

    # CE 핀 비활성화
    GPIO.output(CE_PIN, GPIO.LOW)

# 메인 함수
def main():
    try:
        initialize()
        while True:
            # 보낼 데이터
            data_to_send = "hello world"

            # 데이터 송신
            transmit_data(data_to_send)
            print("Data transmitted:", data_to_send)
            time.sleep(1)  # 1초 대기 후 다음 데이터 전송

    except KeyboardInterrupt:
        spi.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
