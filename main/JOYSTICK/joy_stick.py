import spidev
import time
import os

import socket
HOST='165.229.185.195'
PORT = 5001

def set_left_stick():
  spi_left=spidev.SpiDev()
  spi_left.open(0,0)
  spi_left.max_speed_hz=1000000   
  return spi

def set_right_stick():
  spi_right=spidev.SpiDev()
  spi_right.open(1,0)
  spi_right.max_speed_hz=1000000   
  return spi_right

def ReadChannel(channel,spi):           
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 


def read():
  spi_left=set_left_stick()
  spi_right=set_right_stick()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
swt_channel = 0  
vrx_channel = 1  
vry_channel = 2  
swt_channel_2 = 0  
vrx_channel_2 = 1  
vry_channel_2 = 2  

delay = 0.1
degree=20


  while True:
    vrx_pos = ReadChannel(vrx_channel,spi_left)  
    vry_pos =abs (ReadChannel(vry_channel,spi_left)-1022)
    swt_val = ReadChannel(swt_channel,spi_left)  

    vrx_pos_2 = ReadChannel(vrx_channel_2)  
    vry_pos_2 = abs(ReadChannel(vry_channel_2) -1023)
    swt_val_2 = ReadChannel(swt_channel_2)  
 
while True:

    if(vrx_pos>=500 and vrx_pos<=510):
    vrx_pos=500
  elif(vrx_pos>=0 and vrx_pos < 3):
    vrx_pos=0
  elif(vrx_pos>=1000 and vrx_pos <=1030):
    vrx_pos=1000
  
  if(vry_pos>=495 and vry_pos<=510):
    vry_pos=500
  elif(vry_pos>=0 and vry_pos < 3):
    vry_pos=0
  elif(vry_pos>=1000 and vry_pos <=1035):
    vry_pos=1000
    
    
  if(vrx_pos_2>=518 and vrx_pos_2 <=528):
    vrx_pos_2=500
  elif (vrx_pos_2>=0 and vrx_pos_2 < 3):
    vrx_pos_2=0
  elif (vrx_pos_2>=1000 and vrx_pos_2<=1030):
    vrx_pos_2=1000
  
  
  if(vry_pos_2>=501 and vry_pos_2<=511):
    vry_pos_2=500
  elif (vry_pos_2>=0 and vry_pos_2<=5):
    vry_pos_2=0
  elif (vry_pos_2>=1000 and vry_pos_2<=1030):
    vry_pos_2=1000
    
  #vrx_pos => yaw   vry_pos => Throthle       vrx_pos_2 => ROLL vry_pos_2 => pitch
  vry_pos=float((vry_pos/1000))
  if(vry_pos >=0.0 and vry_pos <=0.2):
    vry_pos=0.2
  elif vry_pos >=0.7:
    vry_pos=0.7
  # vrx_pos=float(((vrx_pos-500)/1000)*degree*2)
  
  # vrx_pos_2=float(((vrx_pos_2-500)/1000)*degree*2)

  # vry_pos_2=float(((vry_pos_2-500)/1000)*degree*2)
  vrx_pos=float(((vrx_pos-500)/500))
  
  vrx_pos_2=float(((vrx_pos_2-500)/500))

  vry_pos_2=float(((vry_pos_2-500)/500))
  mode=""
  if(swt_val <300):
    mode="stop"
  else:
    mode="0"
  if (swt_val<300):
    mode="1"
  msg=f"{vrx_pos} {vry_pos} {vrx_pos_2} {vry_pos_2} "+mode  #yaw throtle  roll pirch

  print(msg)
  sock.sendall(msg.encode())

  time.sleep(delay)
  
  
