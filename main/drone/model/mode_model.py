

class ModeModel():
    def __init__(self):
        self.__mode = 0
    
    def set_mode(self, mode):
        self.__mode = mode
        return

    def get_mode(self):
        return self.__mode