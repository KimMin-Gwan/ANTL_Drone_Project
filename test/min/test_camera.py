import cv2

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    print(type(frame[0][0][0]))
    if ret:
        cv2.imshow("Camera", frame)  # 창 제목


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
camera.release()