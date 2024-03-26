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
FLUSH_TX = 0xE1
NOP = 0xFF

# nRF24L01 레지스터 주소 정의
TX_ADDR = 0x10

# 함수: 레지스터 읽기
def read_register(address):
    return spi.xfer([R_REGISTER | address, NOP])[1:]

# 함수: 초기화 및 설정
def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CE_PIN, GPIO.OUT)
    GPIO.output(CE_PIN, GPIO.LOW)

# 메인 함수
def main():
    try:
        initialize()

        # TX 주소 읽기
        tx_address = read_register(TX_ADDR)

        print("TX Address:", tx_address)

    except KeyboardInterrupt:
        spi.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()