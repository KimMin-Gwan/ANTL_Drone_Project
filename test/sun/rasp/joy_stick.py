import spidev
import time
import os

spi = spidev.SpiDev()     
spi.open(0,0)
spi.max_speed_hz=1000000   

spi_2 = spidev.SpiDev()     
spi_2.open(1,0)
spi_2.max_speed_hz=1000000   

def ReadChannel_2(channel):           
  adc = spi_2.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
def ReadChannel(channel):           
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0  
vrx_channel = 1  
vry_channel = 2  

swt_channel_2 = 0  
vrx_channel_2 = 1  
vry_channel_2 = 2  

delay = 0.1  

while True:

  vrx_pos = ReadChannel(vrx_channel)  
  vry_pos = ReadChannel(vry_channel) 
  swt_val = ReadChannel(swt_channel)  

  vrx_pos_2 = ReadChannel_2(vrx_channel_2)  
  vry_pos_2 = ReadChannel_2(vry_channel_2) 
  swt_val_2 = ReadChannel_2(swt_channel_2)  

  
  print("first    X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,swt_val)) 
  #print("second   X : {}  Y : {}  Switch : {}".format(vrx_pos_2,vry_pos_2,swt_val_2)) 

  time.sleep(delay)
def cal():
  stick_value = 500  # 스틱의 값 (0에서 1000 범위)
min_stick_value = 0
max_stick_value = 1000
min_angle = -45  # 최소 각도
max_angle = 45   # 최대 각도

# 값의 정규화
normalized_value = ((stick_value - min_stick_value) / (max_stick_value - min_stick_value)) * 2 - 1

# 각도로 변환
angle_degrees = normalized_value * max_angle

print(angle_degrees)  # 결과 출력