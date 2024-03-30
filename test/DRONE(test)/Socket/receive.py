import socket
from information import *
import time
class Receive():
    def __init__(self,interface) -> None:
        print("RECEVIED SOCKET START")
        self.Rx_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.Rx_socket.bind((VMWARE_HOST,VMWARE_PORT))  #받는거니까 내가 server로 여는거고
        self.data=None 
        self.addr=None 
        self.interface=interface 
    def receive_data(self):  #thread 로 동작할 함수 
        while True:
            self.data,self.addr=self.Rx_socket.recvfrom(1024) 
            self.data=(self.data.decode().split(":"))
            self.interface.set_euler_angle(float(self.data[0]),float(self.data[1]),float(self.data[2]),float(self.data[3]),self.data[4]) #roll , throttle, yaw , pitch, mode
            time.sleep(0.1)
             
        
        