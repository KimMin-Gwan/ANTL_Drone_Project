import socket




def receive_from_A():
    # A 컴퓨터와 통신할 소켓을 생성합니다.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # 예시 포트 번호 12345
    server_socket.listen(1)
    print("Waiting for connection from A...")
    conn, addr = server_socket.accept()
    print("Connected to A:", addr)
    
    # A로부터 데이터를 받습니다.
    data = conn.recv(1024)  # 최대 1024바이트의 데이터를 받습니다.
    conn.close()  # A와의 연결을 종료합니다.
    server_socket.close()  # 서버 소켓을 닫습니다.
    
    return data

def send_to_B(data):
    # B 컴퓨터와 통신할 소켓을 생성합니다.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('B_IP_address', 12346))  # B의 IP 주소와 포트 번호를 입력합니다.
    
    # 데이터를 B로 전송합니다.
    client_socket.sendall(data)
    client_socket.close()  # B와의 연결을 종료합니다.

# A로부터 데이터를 받습니다.


# 소켓 생성



#HOST='165.229.185.195'
HOST='192.168.50.71'
PORT =65432
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST,PORT))

HOST_2='192.168.232.134'
PORT_2=65433
sock_2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    data,addr=sock.recvfrom(1024)
    print("수신한 데이터",data.decode(),'from',addr)
    sock_2.sendto(data.encode(),(HOST_2,PORT_2))






