import cv2
import pyrealsense2.pyrealsense2 as rs

def main():
    # RealSense pipeline 설정
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

    # RealSense 카메라 시작
    pipeline.start(config)

    try:
        while True:
            # RealSense 프레임 읽기
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            
            # 프레임 데이터를 numpy 배열로 변환
            color_image = np.asanyarray(color_frame.get_data())

            # 화면에 표시
            cv2.imshow('RealSense Camera', color_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        # 리소스 해제
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
