from Drone import *
from Manual import *
import socket
import asyncio
from mavsdk import System
class controller():
    def __init__(self,drone,con_sock) -> None:  #main에서 drone객체 생성후 전달하고 main 에서 con_sock열어서 전달함
        
        self.antl_dron=drone  #드론 객체 전달받았고
        self.sock=con_sock
        self.data=None 

        self.roll=None
        self.throttle=None
        self.pitch=None
        self.yaw=None
        self.mode_type=None        
        self.manual_drone=manual(drone)
        
    async def controll_dron(self):  #thread로 동작해야할 함수 
        #### Yaw Pitch Roll Throttle mode를 계속해서 받아서 mode에 따라서 드론 조종방식을 계속해서 바꾸어준다.
        while True:
            self.data,addr=self.sock.recvfrom(1024)
            my_data=(self.data.decode().split(":"))
            
            self.roll=(float(my_data[0]))
            self.throttle=float(my_data[1])
            self.yaw=(float(my_data[2]))
            self.pitch=(float(my_data[3])) 
            self.mode_type=(my_data[4])
            if(self.mode_type=="stop"):
                pass
            elif(self.mode_type=="man"): #manual_mode 조종
                print(self.throttle)
                self.manual_drone.manul_controls(self.pitch, self.yaw, self.throttle, self.roll)
            elif(self.mode_type=="det"):  #detection mode 조종
                pass
    def start_async_controll_drone(self):
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.controll_dron())
        loop.close()
        
        
    
    