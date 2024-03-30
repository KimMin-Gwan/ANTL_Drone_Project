import socket
import numpy
import cv2

UDP_IP = "165.229.185.195"
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

s = [b'\xff' * 46080 for x in range(20)]     # 640*480*3 을 총 20개로 나눠서 보냄 udp 최대 용량때문에 

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

while True:
    picture = b''

    data, addr = sock.recvfrom(46081)
    s[data[0]] = data[1:46081]
    if data[0] == 19:  #맨마지막 flag오면 
        for i in range(20):
            picture += s[i]  #다합쳐

        frame = numpy.fromstring(picture, dtype=numpy.uint8)
        frame = frame.reshape(480, 640, 3)
        cv2.imshow("frame", frame)
        out.write(frame)

        #message = "hello_client"
        #sock.sendto(message.encode(), addr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            sock.close()
            break
    
    