from model.pilot_model import PilotModel
from model.pilot_model import Drone
import asyncio

from mavsdk import System   
class PilotController:
    def __init__(self):
        self.__pilot_model = PilotModel()
        self.__drone=Drone()

    async def run(self):
        while True:
            mode_type=self.__pilot_model.get_mode()
            (yaw,throttle,pitch,roll)=self.__pilot_model.get_key()
            
            if mode_type=="0":
                await self.__drone.get_drone().manul_control.set_manual_control_input(pitch,yaw,throttle,roll)
            elif mode_type=="1":
                await self.__drone.get_drone().action.land()  #land 함수
            elif mode_type=="2":
                pass

    def set_key(self, key):
        self.__pilot_model.set_key(key=key)
        return
        
    