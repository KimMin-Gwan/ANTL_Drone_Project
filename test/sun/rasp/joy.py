import spidev
import time
import os

spi = spidev.SpiDev()     
spi.open(0,0)
spi.max_speed_hz=1000000   


def ReadChannel(channel):           
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0  
vrx_channel = 1  
vry_channel = 2  


delay = 0.1  

while True:

  vrx_pos = ReadChannel(vrx_channel)  
  vry_pos = ReadChannel(vry_channel) 
  swt_val = ReadChannel(swt_channel)  


 
  print("first    X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,swt_val)) 

  time.sleep(delay)