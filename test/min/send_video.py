from fastapi import FastAPI, Response
import cv2
from fastapi.responses import StreamingResponse


app = FastAPI()


def generate_frames():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ret, buffer = cv2. imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")

