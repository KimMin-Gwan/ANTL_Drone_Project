import spidev
import time
import os

import socket
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


# 서버 주소와 포트
HOST = '165.229.185.195'
PORT = 65432
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
  msg=f"Y:{vrx_pos}T:{vry_pos}P:{vrx_pos_2}R:{vry_pos_2}"
  sock.sendto(msg.encode(),(HOST,PORT))
  time.sleep(delay)
  
  
