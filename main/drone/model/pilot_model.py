
import asyncio
from mavsdk import System
class Drone:
    def __init__(self) -> None:
        self.antl_drone = None
        pass

    async def make_drone(self):
        self.antl_drone=System()
        await self.antl_drone.connect(system_address="serial:///dev/ttyAMA0")
        
        print("Wating for drone to connect...")  #drone connect 
        async for state in self.antl_drone.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone!")
                break
               # Checking if Global Position Estimate is ok
        #async for health in self.antl_drone.telemetry.health():
            #if health.is_global_position_ok and health.is_home_position_ok:
                #print("-- Global position state is good enough for flying.")
                #break
        print("-- Arming")
        await self.antl_drone.action.arm()
        await asyncio.sleep(3)
        await self.antl_drone.manual_control.set_manual_control_input(
        float(0), float(0), float(0.3), float(0)
    )
        #print("--take off")
        #await self.antl_drone.action.takeoff()
        #await asyncio.sleep(4)
        
    
    
    def get_drone(self):
        return self.antl_drone
    

    
    
    
class PilotModel:
    def __init__(self):
        self.__key = Key()
        self.__mode = 0

    def set_mode(self, mode):  
        self.__mode = mode
        return

    # key = ['0.1', '0.1', '0.1', '0.1']
    def set_key(self, key):
        try:
            self.__key.set_key(
                yaw=key[0], throttle=key[1], 
                pitch=key[2], roll=key[3]
                )
        except:
            print("ERROR :: Bad key request")
            self.__key.set_key(
                yaw=0, throttle=0.5, 
                pitch=0, roll=0
                )
        return 
    
    def get_key(self):
        return self.__key.get_key()
    
    def get_mode(self):
        return self.__mode

class Key:
    def __init__(self):
        self.__yaw = 0
        self.__throttle = 0
        self.__pitch = 0
        self.__roll = 0
    ##set
    def set_key(self,yaw,throttle,pitch,roll):
        self.__yaw=yaw
        self.__throttle=throttle
        self.__pitch=pitch
        self.__roll=roll
    ##get
    def get_key(self):
        return (self.__yaw,self.__throttle,self.__pitch,self.__roll)


