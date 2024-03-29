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
  data = ((adc[1]&15) << 8) + adc[2]
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

  # if(vrx_pos>=0 and vrx_pos<3) :
  #   vrx_pos=0
  # if(vrx_pos>=1000):
  #   vrx_pos=1000
  # if(vrx_pos>=498 and vrx_pos <=510)  :
  #   vrx_pos=500
  # if(vry_pos>=0 and vry_pos<3) :
  #   vry_pos=0
  # if(vry_pos>=1000):
  #   vry_pos=1000
  # if(vry_pos>=500 and vry_pos<=521):
  #   vry_pos=500
  # vrx_pos=(vrx_pos-500)/1000
  # vry_pos=(vry_pos-500)/1000
  # vrx_pos= vrx_pos*60
  # vry_pos=vry_pos*60
  
  #print("first    X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,swt_val)) 
  print("second   X : {}  Y : {}  Switch : {}".format(vrx_pos_2,vry_pos_2,swt_val_2)) 

  time.sleep(delay)