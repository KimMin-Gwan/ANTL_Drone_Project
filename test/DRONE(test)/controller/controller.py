
import socket
import asyncio
from mavsdk import System
from Manual import *


class Controller():
    def __init__(self,interface,drone) -> None:
        self.interface=interface  #main 에서 interface만들어서 전달한다.
        self.drone=drone.get_drone()  #main에서 drone생성해서 전달
        self.my_data=None
        self.manul_mode= Manual(self.drone)
    
    async def controll_dron(self):   #비동기로 계속 돌리고 
        while True:  #다른 스레드에서 드론 만드는거 기다리고 
            print("waitting drone making .....")
            await asyncio.sleep(1)
            if(self.interface.get_drone_flag() == 1):
                break
        print("start drone controll")
        while True:
            
            (mode_type,pitch,yaw,throttle,roll)=self.interface.get_euler_angle()
            if(mode_type=="man") :  #manual모드로 비행기 조종한다.
                await self.drone.manual_control.set_manual_control_input(pitch,yaw,throttle,roll)
                #await self.manul_mode.manul_controls(pitch,yaw,throttle,roll) 
            elif(mode_type=="stop"):
                await self.drone.action.land()

        