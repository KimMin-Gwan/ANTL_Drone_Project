from model import PilotModel
from model import Drone
import asyncio

from mavsdk import System   
class PilotController:
    def __init__(self, mode):
        self.__mode = mode
        self.__pilot_model = PilotModel()
        self.__drone=Drone()

    async def init_drone(self):
        await self.__drone.make_drone()


    async def run(self):
        while True:
            mode_type=self.__mode.get_mode()
            (yaw,throttle,pitch,roll)=self.__pilot_model.get_key()
            print("----",throttle)
            if mode_type==0:
                #print(yaw,throttle,pitch,roll)
                await self.__drone.get_drone().manual_control.set_manual_control_input(pitch,yaw,throttle,roll)
            elif mode_type==1:
                pass
                #await self.__drone.get_drone().action.land()  #land 함수
            elif mode_type==2:
                pass


    def set_key(self, key):
        self.__pilot_model.set_key(key=key)
        return
        
    