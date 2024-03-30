import drone
import Manual
import Socket
import interface

import information
import controller
import asyncio
from threading import Thread


class Main_Function():
    def __init__(self):
        print("SYSTEM ALAM :: ANTL - DRONE SYSTEM ON")
        self.interface=interface.Interface()
        self.receive=Socket.Receive(self.interface)  #나중에 받는 부분 스레드로 시작해야함  thread -> async function sequence
        self.drone=drone.Drone(self.interface)  #일단 만들고 나중에 async함수로 드론 만들기 시작해야함 
        self.drone_controller=None
    
    
    async def make_drone(self):
        print("SYSTEM ALARM : MAKING DRONE....")
        await self.drone.make_drone()  #드론을 만들어야함
        self.drone_controller=controller.Controller(self.interface,self.drone) 
    async def start_drone_controll(self):
        await self.drone_controller.controll_dron()
        
    def start_system(self):

        asyncio.run(self.make_drone())
        receive_thread=Thread(target=self.receive.receive_data)
        receive_thread.start() #스레드 먼저 돌리고
        #asyncio.run(self.start_drone_controll())
        


