import asyncio
import random
import socket
from mavsdk import System
class Manual():
    def __init__(self,drone) -> None:
        self.drone=drone  #drone class말고 드론 그 자체를 받아서
    
    
    
    
    
    async def manul_controls(self,pitch,yaw,throttle,roll):
        await self.drone.manual_control.set_manual_control_input(
           pitch,yaw,throttle,roll 
        )
        await asyncio.sleep(0.001)