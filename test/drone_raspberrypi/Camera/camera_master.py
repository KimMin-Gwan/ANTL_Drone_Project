from Information import *
class camera():
    def __init__(self,camera_sock) -> None:
        self.camera_data="adsf\n"
        self.sock=camera_sock

    def send_FPV(self):
        while True:
           self.sock.sendto(self.camera_data.encode(),(ANTL_HOST,ANTL_PORT))
    
        