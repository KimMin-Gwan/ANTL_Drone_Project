

class PilotModel:
    def __init__(self):
        self.__key = Key()
        self.__mode = 0

    def set_mode(self, mode):  
        self.__mode = mode
        return

    def set_key(self, key):

        return 
    
    def get_key(self):
        return self.__key
    
    def get_mode(self):
        return self.__mode

class Key:
    def __init__(self):
        self.__yaw = 0
        self.__throttle = 0
        self.__pitch = 0
        self.__roll = 0

    ##set
        
    ##get



