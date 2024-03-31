import cv2
import numpy as np
import time
from typing import Any
#from tensorflow.lite.python.interpreter import Interpreter
import tflite_runtime.interpreter as tflite
import pyrealsense2.pyrealsense2 as rs
import os
import re
from PIL import Image
import collections
from threading import Thread
import platform

import time

PATH_TO_MODEL = "/home/pi/ANTL_DRONE_Project/main/drone/mobilenet_ssd/"
MODEL = "mobilenet_ssd_v2_coco_quant_postprocess.tflite"
TPU_MODEL = "mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
PATH_TO_LABEL = "/home/pi/ANTL_DRONE_Project/main/drone/mobilenet_ssd/coco_labels.txt"

EDGETPU = True

MIN_CONF_THRESHOLD = 0.5  # 최소값
SELECT_OBJ = "car"  # 타겟
TOP_K = 5  # 보여주는 오브젝트 갯수
FONT =cv2.FONT_HERSHEY_SIMPLEX
MIN_COUNT = 30

EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': "edgetpu.dll"
}[platform.system()]

WAIT_IMG_PATH = "/home/pi/ANTL_DRONE_Project/main/drone/model/wait_img.png"



#TEST_FLAG = (True, )
TEST_FLAG = (False, )

OBJECT = 1
FRONT = 2

DEFAULT = False
REPLACEMENT = True

class ModeModel():
    def __init__(self):
        self.__mode = 0
    
    def set_mode(self, mode):
        self.__mode = mode
        return

    def get_mode(self):
        return self.__mode

camera= cv2.VideoCapture(0)

class VideoModel():
    def __init__(self):
        self.__wait_img = cv2.imread(WAIT_IMG_PATH)
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
        ret, self.__frame = camera.read()
        if not ret:
            print("Camera Error")
        return

    def get_frame(self):
        return self.__frame
    
    def get_raw_frame(self):
        return self.__raw_frame

    

    def get_frame_bytes(self):
        try:
            _, buffer = cv2.imencode('.jpg', self.__frame)
            frame = buffer.tobytes()
        except:
            _, buffer = cv2.imencode('.jpg', self.wait_img)
            frame = buffer.tobytes()
        return frame
    


class VideoController:
    def __init__(self, video_model):
        # hand camera init
        print("SYSTEM ALARM::Camera Configure initiating")
        self.__model:VideoModel = video_model

        # Configure depth and color streams
        self.pipeline = rs.pipeline()  # intel realsense capture
        self.config = rs.config()  # intel realsense configuration
        self.__init_realsense()

        self.status = FRONT # 1: front , 2: object 
        self.swap_flag = DEFAULT  # false: default, true: for replacement
        print("SYSTEM ALARM::Camera Configure Initiating Complete")

    # realsense 초기화
    def __init_realsense(self):
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        # RGB & Depth
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # 카메라 ON
    def run_camera(self):
        # webcam(기본값) 스레드 실행
        self.pipeline.start(self.config) #self.info.setSystemState(newSystem)
        self.thread = Thread(target=self.run_front_cam, args=(TEST_FLAG))  # True로 해둬야 테스트 과정에서 화면 확인 O (없을 시 스레드 종료 불가)
        self.thread.start()
        self.status = FRONT # 1: front , 2: object 
        return

    # 카메라 전환 함수
    def swap_camera(self):
        # 그냥 join 해버리니까 스레드 종료과정에서 StartCam 내부의 while 부근에서 오류가 남
        # 그래서 플래그를 세워 StartCam 내부의 while 문을 종료시켜서 끌 것
        self.swap_flag = REPLACEMENT  # 기본 flag == 0, 멈추려고 할 때는 flag == 1로 설정해주기

        time.sleep(0.5)
        # object → front 
        if self.status == OBJECT:  # Now: front
            print('SYSTEM ALARM::START HAND CAM')
            self.swap_flag = DEFAULT
            self.thread = Thread(target=self.run_front_cam, args=(TEST_FLAG))  # True로 해둬야 테스트 과정에서 화면 확인 O (없을 시 스레드 종료 불가)
            self.thread.start()
            self.status = FRONT # Change Cam's status; web > hand
        
        # front → object 
        else:
            print('SYSTEM ALARM::START WEB CAM')
            self.swap_flag = DEFAULT
            self.pipeline.start(self.config)
            self.thread = Thread(target=self.run_object_cam, args=(TEST_FLAG))  # True로 해둬야 테스트 과정에서 화면 확인 O (없을 시 스레드 종료 불가)
            self.thread.start()
            self.status = OBJECT # Change Cam's status; hand > web
        return

    # front cam ON;  flag를 True로 하면 화면에 출력이 나옴
    def run_front_cam(self, flag = False):

        #while self.handcam.isOpened():  # 카메라가 켜졌을 때
        while True:
            if self.swap_flag == REPLACEMENT:  # web에서 swap cam 버튼이 눌려 flag 0 > 1 변경, 카메라 전환을 하겠다는 의미
                break

            self.__model.capture_frame()

            if flag:
                cv2.imshow("Camera", self.__model.get_frame())  # 창 제목
    
                if cv2.waitKey(1) & 0xFF == ord('q'):  # q 누르면 나가기
                    break
            
        print("SYSTEM ARAM::Terminate Handcam")

    # Real Sence ON
    def run_object_cam(self, flag = False):
        ## License: Apache 2.0. See LICENSE file in root directory.
        ## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.
        # Configure depth and color streams
        # depth cam 제외, rgb 카메라만 사용할 수 있도록 기본 코드에서 수정.
        
        self.__model.set_frame2wait_image()
        raw_frame = None
        while True:
            if self.swap_flag == REPLACEMENT:  # web에서 swap cam 버튼이 눌려 flag 0 -> 1 변경, 카메라 전환을 하겠다는 의미
                break
            
            # Wait for a frame : color
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            # Convert image to numpy array
            raw_frame = np.asanyarray(color_frame.get_data())

            self.__model.set_raw_frame(raw_frame)
            
            if flag:  # flag == 1로 설정 시(기본값 0) window에 카메라 화면 창 띄우기
                # Show RGB image
                cv2.namedWindow('RGB Camera', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RGB Camera', self.__model.get_raw_frame())
                cv2.waitKey(1)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):  # q 키 누르면 카메라 창을 종료하도록 설정 후 핸드캠으로 전환됨
                    break
            
        if flag:  # flag == 1로 설정 시(기본값 0) window에 띄워진 카메라 화면 창 닫기
            cv2.destroyAllWindows()

        print("SYSTEM ARARM::Terminate Webcam")
        # Stop streaming
        self.__model.set_frame2wait_image()          
        self.pipeline.stop()
       

class VideoModel():
    def __init__(self):
        self.__wait_img = cv2.imread(WAIT_IMG_PATH)
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
        ret, self.__frame = camera.read()
        if not ret:
            print("Camera Error")
        return

    def get_frame(self):
        return self.__frame
    
    def get_raw_frame(self):
        return self.__raw_frame

    

    def get_frame_bytes(self):
        try:
            _, buffer = cv2.imencode('.jpg', self.__frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

            frame = buffer.tobytes()
        except:
            _, buffer = cv2.imencode('.jpg', self.__wait_img, [cv2.IMWRITE_JPEG_QUALITY, 90])
            frame = buffer.tobytes()
        return frame
    

    
class Image_Manager:
    def __init__(self):
        self.frame = None # 3차원 행렬
        self.width = 0
        self.height = 0
        self.init_flag = False
        
    # 이번 루프에서 프레임 특징
    def recog_image(self, frame):
        self.frame = frame
        #self.frame = cv2.flip(self.frame, 0)
        #self.frame= cv2.flip(self.frame, 1)
        cv2_im_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        # 최초에 한번만 연산
        if not self.init_flag:
            self.height, self.width, _ = frame.shape
            self.init_flag == True
            
        return self.width, self.height, pil_im
    
    def show_test_window(self):
        cv2.imshow('test_window', self.frame)
        return

    def get_frame(self):
        return self.frame
    
    def set_frame(self, frame):
        self.frame = frame

    #def depth_draw(self, x, y, depth):
        #self.frame = self.bbox_manager.draw_depth_in_image(self.frame, x, y, depth)
        #return 

    # bbox 만들기
    def append_text_img(self, objs, labels, dur):
        height, width, _= self.frame.shape

        #fps=round(100/dur,1)
        #fps 조정 = 1000/전체 작동시간

        self.frame= cv2.rectangle(self.frame, (0,0), (width, 24), (0,0,0), -1)
        #cv2 외부 틀만들기

        text1 = 'FPS: {}'.format(dur)
        self.frame = cv2.putText(self.frame, text1, (10, 20),FONT, 0.7, (0, 0, 255), 2)
        #cv2. 영상에 FPS 띄우기

        #아래는 대충 사각형으로 오브젝트를 감싸는 내용
        for obj in objs:
            x0, y0, x1, y1 = list(obj.bbox)
            x0, y0, x1, y1 = int(x0*width), int(y0*height), int(x1*width), int(y1*height)
            percent = int(100 * obj.score)
            
            if (percent>=60):
                box_color, text_color, thickness=(0,255,0), (0,255,0),2
            elif (percent<60 and percent>40):
                box_color, text_color, thickness=(0,0,255), (0,0,255),2
            else:
                box_color, text_color, thickness=(255,0,0), (255,0,0),1
                
        
            text3 = '{}% {}'.format(percent, labels.get(obj.id, obj.id)) #얼마나 일치하는지 표시
        
            self.frame = cv2.rectangle(self.frame, (x0, y0), (x1, y1), box_color, thickness)
            self.frame = cv2.putText(self.frame, text3, (x0, y1-5),FONT, 0.5, text_color, thickness)
        return 
    
        
Object = collections.namedtuple('Object', ['id', 'score', 'bbox']) #오브젝트 라는 튜플 서브 클래스

class BBox(collections.namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])):
    __slots__ = ()

class Tools:
    # 생성자
    def __init__(self):
        self.__load_model()
        pass

    def __load_model(self):
        self.__set_interpreter_tpu()
        self.__input_image_size()
        self.interpreter.allocate_tensors()
        self.labels = self.__load_labels()

    # 모델 세팅
    def __set_interpreter_tpu(self, model_file=PATH_TO_MODEL+TPU_MODEL):
        model_file, *device = model_file.split('@')
        self.interpreter = tflite.Interpreter(
            model_path=model_file,
            experimental_delegates=[
                tflite.load_delegate(EDGETPU_SHARED_LIB,
                                     {'device':device[0]} if device else {})
            ]
        )

    # 이미지 인풋
    def set_input(self, image, resample=Image.NEAREST):
        image = image.resize((self.width, self.height), resample)
        self.__input_tensor()[:,:] = image
        self.interpreter.invoke()
        #tensor_index = self.input_detail['index']
        #input = self.interpreter.tensor(tensor_index)()[0]
        #return input
    
    # 넘파이로 변환
    def __input_tensor(self):
        tensor_index = self.input_detail['index']
        return self.interpreter.tensor(tensor_index)()[0]

    # 텐서 인풋 세팅
    def __input_image_size(self):
        self.input_detail = self.interpreter.get_input_details()[0]
        self.height= self.input_detail['shape'][1]
        self.width = self.input_detail['shape'][2]
        self.channels = self.input_detail['shape'][3]

    # 연산결과  반환
    def output_tensor(self, i):
        """한번 양자화된 데이터라면 양자화를 해제한다."""
        output_details = self.interpreter.get_output_details()[i]
        output_data = np.squeeze(self.interpreter.tensor(output_details['index'])()) #실제로 사용중인 배열의 차원수를 줄여줌
        """만약 3차원 배열일때, 반드시 n차원일 필요가 없다면 명시적으로 분석하기 편한 n-x (x<n) 차원배열로 바꿀수 있다.
        ex) [[1,2,3]] => [1,2,3] (2차원배열이지만 굳이 2차원배열일 필요가 없기에 1차원 배열로 바꾸었다)
        """

        if 'quantization' not in output_details: #만약 세부정보가 양자화 되지 않았다면 바로 데이터를 반환
            return output_data

        scale, zero_point = output_details['quantization'] #양자화된 데이터의 scale(범위)와 zero_point(영점)을 받아온다.
        if scale == 0: #만약 범위가 양자화를 하나 마나 똑같다면 
            return output_data - zero_point #데이터를 영점에서 뺀 값을 돌려줌

        return scale * (output_data - zero_point) #위의 상황이 아니라면 범위와 영점을 이용하여 원래 값으로 양자화 해제한다.
    
    def __load_labels(self):
        p = re.compile(r'\s*(\d+)(.+)') #이거 대충 띄어쓰기 같은건데 정규식으로 반환된거 내용을 아래에서 match함수로 긁어올꺼라서 그럼
        with open(PATH_TO_LABEL, 'r', encoding='utf-8') as f:
            lines = (p.match(line).groups() for line in f.readlines()) #라벨 폴더에서 한줄씩 긁어옴
            return {int(num): text.strip() for num, text in lines} #한줄씩 긁어온 내용의 복사본을 반환(딕셔너리)
        
    def get_labels(self):
        return self.labels

    def get_output(self, top_k=TOP_K, image_scale=1.0):
        """Returns list of detected objects."""
        boxes = self.output_tensor(0)
        class_ids = self.output_tensor(1)
        scores = self.output_tensor(2)
        #count = int(self.output_tensor(self.interpreter, 3))
        #박스의 크기, 오브젝트의 아이디(사물의 이름), 얼마나 비슷한지, 몇개 인지


        def make(i): #박스의 크기 제단한 내용을 리턴할 것인데 아래의 make 함수를 재귀하여 사용
            #(재귀하기 때문에 지역변수 사용을 위해 get_output 함수 안에 작성)
            ymin, xmin, ymax, xmax = boxes[i]
            return Object(
                id=int(class_ids[i]),
                score=scores[i],
                bbox=BBox(xmin=np.maximum(0.0, xmin),
                        ymin=np.maximum(0.0, ymin),
                        xmax=np.minimum(1.0, xmax),
                        ymax=np.minimum(1.0, ymax)))

        return [make(i) for i in range(top_k) if scores[i] >= MIN_CONF_THRESHOLD] #재귀해서 리턴시킴
        

class ObjectFollower:
    def __init__(self, key):
        self.__key:list = key
        pass

    def check_object(self, objs, frame):
        height, width, _ = frame.shape
        frame_y_middle = height/2
        frame_x_middle = width/2
        y_max = frame_y_middle / 2


        for obj in objs:
            x0, y0, x1, y1 = list(obj.bbox)
            x0, y0, x1, y1 = int(x0*width), int(y0*height), int(x1*width), int(y1*height)
            percent=(100*obj.score)

            if percent < 40:
                continue

            try:
                y_middle = (y1 + y0) / 2
                x_middle = (x1 + x0) / 2

                y_diff = frame_y_middle - y_middle
                x_diff = x_middle - frame_x_middle 
                yaw = 0
                pitch = 0
                roll = 0

                if y_max < abs(y_diff):
                    # yaw를 바꿔야함
                    # pitch를 바꿔야함
                    pitch = y_diff / height
                    if abs(x_diff) < 50:
                        yaw = 0
                    else:
                        yaw = x_diff / width
                else:
                    # roll을 바꿔야함
                    roll = x_diff / width
                self.__key = [yaw, 0.5, pitch, roll]
            except:
                self.__key = [0, 0.3, 0, 0]
        return



class ObjectController:
    def __init__(self, video_model, mode):
        self.__key = []
        self.__video_model:VideoModel = video_model# 카메라 정보 
        self.__mode:ModeModel = mode
        self.status = 0 # 0 : 정지, 1 : 동작, 2 : 일시정지
        self.pause_flag = False
        self.tool = Tools() # 로드 모델, 로드 라벨, 텐서 세팅

        self.image_manager = Image_Manager()
        self.__object_follower = ObjectFollower(key=self.__key) # 검색 시작

    def __human_detection(self):
        # 라벨 세팅
        #distance = []
        fps = 1
        #반복되는 핵심 와일문
        while True:

            # 일시정지 상태
            if not self.__mode.get_mode():
                continue

            start_time = time.time()            
            frame = self.__video_model.get_raw_frame()
            _, _, pil_im = self.image_manager.recog_image(frame)

            # 연산 부분
            self.tool.set_input(pil_im)
            objs = self.tool.get_output() # obj 탐색

            # output을 바탕으로 사용가능한 bbox인지 체크 및 그리기
            
            # 발견한 오브젝트의 거리를 분석
            try:
                self.__object_follower.check_object(objs=objs, frame=frame)
            except Exception as e:
                print("ERROR :: follower did not work")
                print(e)

            fps = round(1.0/(time.time() - start_time), 1)
            self.image_manager.append_text_img(objs=objs,
                                               labels=self.tool.get_labels(),
                                               dur=fps)          
            # bbox된 이미지 데이터를 다시 카메라 프레임으로 설정
            bboxed_frame = self.image_manager.get_frame()
            self.__video_model.set_frame2bboxed_frame(bboxed_frame)
    
    # 실행기
    def run_object_detector(self):
        self.status = 1 # 텐서 연산을 한다 : 1, 안한다 : 2
        human_detector_thread = Thread(target=self.__human_detection)
        human_detector_thread.start()
    
import socket # 소켓 프로그래밍에 필요한 API를 제공하는 모듈
import struct # 바이트(bytes) 형식의 데이터 처리 모듈
import pickle # 객체의 직렬화 및 역직렬화 지원 모듈

def server_send(video_model:VideoModel):
    # 서버 ip 주소 및 port 번호
    ip = '192.168.14.130'
    port = 5001


    # # 소켓 객체 생성
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    #     # 서버와 연결
    #     client_socket.connect((ip, port))
        
    #     print("연결 성공")
        
    #     # 메시지 수신
    #     while True:
    #         # 프레임 읽기
    #         frame = video_model.get_frame_bytes()
            
    #         frame = pickle.dumps(frame)

    #         client_socket.sendall(struct.pack(">L", len(frame)) + frame)
    sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    while True:
        frames=video_model.get_frame_bytes()
        #color_frame=frames.get_color_frame()
        color_image=np.asanyarray(frames)
        d = color_image.flatten()
        s = d.tostring()
        for i in range(20):
            sock.sendto(bytes([i]) + s[i*46080:(i+1)*46080], (ip, port))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    video_model = VideoModel()
    mode_model = ModeModel()
    thread = Thread(target=server_send, args=(video_model, ))
    thread.start()
    video_controller = VideoController(video_model=video_model)
    object_controller = ObjectController(video_model=video_model, mode=mode_model)
    video_controller.run_camera()
    object_controller.run_object_detector()


