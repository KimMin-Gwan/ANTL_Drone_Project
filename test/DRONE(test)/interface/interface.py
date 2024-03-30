class Interface():
    def __init__(self) -> None:
        self.roll=None
        self.throttle=None
        self.yaw=None
        self.pitch=None
        self.mode_type=None
        self.make_dorne=False
        self.drone_power_flag="ON"
    def set_euler_angle(self,roll,throttle,yaw,pitch,mode):
        self.pitch=pitch
        self.yaw=yaw
        self.throttle=throttle
        self.roll=roll
        self.mode_type=mode
        
    def get_euler_angle(self):
        return (self.mode_type,self.pitch,self.yaw,self.throttle,self.roll)
    
    def set_drone_flag(self,flag):
        self.make_dorne=flag
        
    def get_drone_flag(self):
        return self.make_dorne
    
    def set_drone_power(self,flag) :
        self.drone_power_flag=flag
        
    def get_drone_power(self):
        return self.drone_power_flag