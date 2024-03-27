## 드론의 상태를 보관 ex) 센서값, 베터리 잔량 등
import cv2
from enum import Enum, auto

class VideoModel:
    def __init__(self):
        self.__frame = None
        self.__raw_frame = None
        self.__cap = cv2.VideoCapture(0)

    def get_cap(self):
        return self.__cap

    def set_frame(self, frame):
        self.__frame = frame

    def set_raw_frame(self, frame):
        self.__raw_frame = frame
    
    def get_frame(self):
        return self.__frame


class PilotModel():
    def __init__(self):
        self.__key = Key()
        self.__mode = Mode.DEFAULT
        self.__Pilot_State = False # 용도 불명

    # key 변경
    def set_key(self, keys:list):
        self.__key.set_x1(keys[0])
        self.__key.set_y1(keys[1])
        self.__key.set_x2(keys[2])
        self.__key.set_y2(keys[3])

    # key 접근
    def get_key(self):
        return self.__key.get_xy()
    
    # 모드 추가예정
    def set_mode(self, mode:int):
        if mode == 0:
            self.__mode = Mode.DEFAULT
        elif mode == 1:
            self.__mode = Mode.MANUAL
        elif mode == 2:
            self.__mode = Mode.AUTO
        else:
            self.__mode = Mode.DEFAULT
    
    # return data = 0, 1, 2 
    def get_mode(self)->int:
        return self.__mode.value

class Mode(Enum):
    DEFAULT = auto()
    MANUAL = auto()
    AUTO = auto()

# 조종기
class Key():
    def __init__(self):
        self.__on_off = 0 # 어디다 쓰는지 모름
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
        return self.__x1, self.__y1, self.__x2, self.__y2