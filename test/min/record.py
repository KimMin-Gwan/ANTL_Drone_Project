import cv2

# 웹캠으로부터 영상 캡처를 시작합니다.
cap = cv2.VideoCapture(0)

# 캡처할 영상의 폭과 높이를 설정합니다.
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 녹화할 동영상 파일을 설정합니다.
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))

# 무한 반복으로 영상을 캡처하고 녹화합니다.
while True:
    ret, frame = cap.read()
    
    # 캡처된 프레임이 정상적으로 반환되면 녹화합니다.
    if ret:
        # 영상을 화면에 표시합니다.
        cv2.imshow('frame', frame)
        
        # 영상을 파일에 저장합니다.
        out.write(frame)
        
        # 'q' 키를 누르면 녹화를 중지합니다.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 모든 작업이 완료되면 객체를 해제합니다.
cap.release()
out.release()
cv2.destroyAllWindows()