import cv2
import numpy as np
import pyrealsense2.pyrealsense2 as rs
import time
import threading
from model import VideoModel

#TEST_FLAG = (True, )
TEST_FLAG = (False, )

OBJECT = 1
FRONT = 2

DEFAULT = False
REPLACEMENT = True


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
        self.thread = threading.Thread(target=self.run_front_cam, args=(TEST_FLAG))  # True로 해둬야 테스트 과정에서 화면 확인 O (없을 시 스레드 종료 불가)
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
            self.thread = threading.Thread(target=self.run_front_cam, args=(TEST_FLAG))  # True로 해둬야 테스트 과정에서 화면 확인 O (없을 시 스레드 종료 불가)
            self.thread.start()
            self.status = FRONT # Change Cam's status; web > hand
        
        # front → object 
        else:
            print('SYSTEM ALARM::START WEB CAM')
            self.swap_flag = DEFAULT
            self.pipeline.start(self.config)
            self.thread = threading.Thread(target=self.run_object_cam, args=(TEST_FLAG))  # True로 해둬야 테스트 과정에서 화면 확인 O (없을 시 스레드 종료 불가)
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
       
    
        
