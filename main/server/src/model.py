import cv2
from constants import WAIT_IMG_PATH

class VideoModel():
    def __init__(self):
        self.__frame = None
        self.__wait_img = cv2.imread(WAIT_IMG_PATH)

    # 프레임 세팅
    def set_frame(self, frame):
        self.__frame = frame

    def get_default_frame(self):
        return self.__wait_img

    # 프레임 호출
    def get_frame(self):
        return self.__frame
    

class PilotModel():
    def __init__(self):
        self.__key = Key()
        self.__Pilot_State = False # 코드로 적을것

    def set_key(self, x1=-1, y1=-1, x2=-1, y2=-1):
        if x1 != -1:
            self.__key.set_x1(x1)
        if x2 != -1:
            self.__key.set_x2(x2)
        if y1 != -1:
            self.__key.set_y1(y1)
        if y2 != -1:
            self.__key.set_y2(y2)

    def get_key(self):
        return self.__key.get_xy()

class Key():
    def __init__(self):
        self.__on_off = 0
        self.__x1 = 0
        self.__y1 = 0
        self.__x2 = 0
        self.__y2 = 0

    def set_x1(self, x):
        self.__x1 = x
        return

    def set_x2(self, x):
        self.__x2 = x
        return

    def set_y1(self, y):
        self.__y1 = y
        return

    def set_y2(self, y):
        self.__y2 = y
        return

    def get_xy(self):
        return self.__x1, self.__x2, self.__y1, self.__y2
        
        

