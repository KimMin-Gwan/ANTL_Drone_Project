import cv2

WAIT_IMG_PATH = "/home/pi/ANTL_Drone_Project/main/drone/model/wait_img.png"


class VideoModel():
    def __init__(self):
        self.__wait_img = cv2.imread(WAIT_IMG_PATH)
        self.__camera = cv2.VideoCapture(0)
        self.__frame = None
        self.__raw_frame = None

    def set_frame2bboxed_frame(self, frame):
        self.__frame = frame

    def set_frame2wait_image(self):
        self.__frame = self.__wait_img
        self.__raw_frame = self.__wait_img
        return

    def set_raw_frame(self, frame):
        self.__raw_frame = frame
        return

    def capture_frame(self):
        ret, self.__frame = self.__camera.read()
        if not ret:
            print("Camera Error")
        return

    def get_frame(self):
        return self.__frame
    
    def get_raw_frame(self):
        return self.__raw_frame

    def get_camera(self):
        return self.__camera
    

    def get_frame_bytes(self):
        try:
            _, buffer = cv2.imencode('.jpg', self.__frame)
            frame = buffer.tobytes()
        except:
            _, buffer = cv2.imencode('.jpg', self.wait_img)
            frame = buffer.tobytes()
        return frame
    