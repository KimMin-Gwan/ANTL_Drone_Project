import asyncio
import random
import socket
from mavsdk import System

class manual():
    def __init__(self,drone) -> None:

        self.antl_drone=drone  #main에서 drone객체 받아와서 조종 해야지
    
    
    async def manul_controls(self,pitch,yaw,throttle,roll):
        await self.antl_drone.manual_control.set_manual_control_input(
           pitch,yaw,throttle,roll 
        )
        await asyncio.sleep(0.01)