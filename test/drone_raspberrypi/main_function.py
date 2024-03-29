import Camera
import Drone
import Information
import Manual
import socket
import DroneController
from threading import Thread
import asyncio
class Main_Function():
    def __init__(self) -> None:
        print("SYSTEM ALAM :: DRONE FUNCTION ON")
        self.Rx_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.Rx_socket.bind((Information.VMWARE_HOST,Information.VMWARE_PORT))  #받는거니까 내가 server로 여는거고
        self.Tx_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.loop=asyncio.get_event_loop()
        self.drone=None
  
        
        self.drone_controller=DroneController.controller(self.drone,self.Rx_socket)
        self.camera=Camera.camera(self.Tx_socket) 
        print("SYSTEM ALARM::Initializing Successfully Finished")
   
    async def create_drone_instance(self):
        self.drone=Drone.drone()
        await self.drone.make_drone()
        
        
    async def start_system(self):
        print("SYSTEM ALARM::System start")
        camera_thread=Thread(target=self.camera.send_FPV)
        camera_thread.start()
        print("====")
        await asyncio.get_event_loop().run_in_executor(None, self.drone_controller.controll_dron)
       
        
async def main():
    main_name=Main_Function()
    await main_name.create_drone_instance()
    await main_name.start_system()
if __name__=="__main__":  #Test용 main
    asyncio.run(main())