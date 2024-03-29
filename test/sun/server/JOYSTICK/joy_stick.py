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
HOST='192.168.50.71' #컴퓨터 시라파이션
PORT = 65432

#HOST='192.168.50.232'  #라파 투 라파
#PORT=65433
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
swt_channel = 0  
vrx_channel = 1  
vry_channel = 2  

swt_channel_2 = 0  
vrx_channel_2 = 1  
vry_channel_2 = 2  

delay = 0.1
degree=20
while True:

  vrx_pos = ReadChannel(vrx_channel)  
  vry_pos =abs (ReadChannel(vry_channel)-1022)
  #swt_val = ReadChannel(swt_channel)  

  vrx_pos_2 = ReadChannel_2(vrx_channel_2)  
  vry_pos_2 = abs(ReadChannel_2(vry_channel_2) -1023)
  #swt_val_2 = ReadChannel_2(swt_channel_2)  
  if(vrx_pos>=500 and vrx_pos<=510):
    vrx_pos=500
  elif(vrx_pos>=0 and vrx_pos < 3):
    vrx_pos=0
  elif(vrx_pos>=1015 and vrx_pos <=1025):
    vrx_pos=1000
  
  if(vry_pos>=495 and vry_pos<=510):
    vry_pos=500
  elif(vry_pos>=0 and vry_pos < 3):
    vry_pos=0
  elif(vry_pos>=1017 and vry_pos <=1027):
    vry_pos=1000
    
    
  if(vrx_pos_2>=518 and vrx_pos_2 <=528):
    vrx_pos_2=500
  elif (vrx_pos_2>=0 and vrx_pos_2 < 3):
    vrx_pos_2=0
  elif (vrx_pos_2>=1017 and vrx_pos_2<=1026):
    vrx_pos_2=1000
  
  
  if(vry_pos_2>=501 and vry_pos_2<=511):
    vry_pos_2=500
  elif (vry_pos_2>=0 and vry_pos_2<=5):
    vry_pos_2=0
  elif (vry_pos_2>=1017 and vry_pos_2<=1028):
    vry_pos_2=1000
    
  #vrx_pos => yaw   vry_pos => Throthle       vrx_pos_2 => ROLL vry_pos_2 => pitch
  vry_pos=float((vry_pos/1000))
  if(vry_pos >=0.0 and vry_pos <=0.2):
    vry_pos=0.2
  elif vry_pos >=0.7:
    vry_pos=0.7
  vrx_pos=float(((vrx_pos-500)/1000)*degree*2)
  
  vrx_pos_2=float(((vrx_pos_2-500)/1000)*degree*2)

  vry_pos_2=float(((vry_pos_2-500)/1000)*degree*2)
  
  msg=f"{vrx_pos}:{vry_pos}:{vrx_pos_2}:{vry_pos_2}"

  print(msg)
  sock.sendto(msg.encode(),(HOST,PORT))
  time.sleep(delay)
  
  
