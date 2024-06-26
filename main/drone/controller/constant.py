import platform
import cv2

PATH_TO_MODEL = "/home/pi/ANTL_Drone_Project/main/drone/mobilenet_ssd/"
MODEL = "mobilenet_ssd_v2_coco_quant_postprocess.tflite"
TPU_MODEL = "mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
PATH_TO_LABEL = "/home/pi/ANTL_Drone_Project/main/drone/mobilenet_ssd/coco_labels.txt"


EDGETPU = True

MIN_CONF_THRESHOLD = 0.7  # 최소값
SELECT_OBJ = "car"  # 타겟
TOP_K = 1  # 보여주는 오브젝트 갯수
FONT =cv2.FONT_HERSHEY_SIMPLEX
MIN_COUNT = 30

EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': "edgetpu.dll"
}[platform.system()]
