class RealTimeAPI:
    def __init__(self, controller):
        self.server_socket = None
        self.data_buffer = b""
        self.video_buffer_size = struct.calcsize("L") # unsigned long
        self.controller = controller

    def __data_send(self, client_socket:Sock):
        try:
           while True:
                frame = self.controller.get_video()
                frame = pickle.dumps(frame)

                client_socket.sendall(struct.pack(">L", len(frame)) + frame)

        except Exception as e:
            print(e)
        return
            
    def __data_recv(self, client_socket:Sock):
        try:
            data_size = struct.calcsize("L")
            while True:
                while len(self.data_buffer) < data_size:
                    self.data_buffer += client_socket.recv(4096)

                packed_data_size = self.data_buffer[:data_size]
                self.data_buffer = self.data_buffer[data_size:]

                frame_size = struct.unpack(">L", packed_data_size)[0]

                while len(self.data_buffer) < frame_size:
                    self.data_buffer += client_socket.recv(4096)
                
                frame_data = self.data_buffer[:frame_size]
                self.data_buffer = self.data_buffer[frame_size:]

                frame = pickle.loads(frame_data)

                # frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                self.controller.set_video(frame)
                
        except Exception as e:
            print(e)
        return

    def __handle_client(self, client_socket):
        send_thread = Thread(target=self.__data_send, args=(client_socket,))
        recv_thread = Thread(target=self.__data_recv, args=(client_socket,))
        send_thread.start()
        recv_thread.start()

    def waiting_client(self, server_socket:Sock):
        self.server_socket = server_socket
        try:
            print("Real-time send system lunching")
            client_socket, client_address = self.server_socket.accept()
            print(f">> Client {client_address} has connected")
            self.__handle_client(client_socket)

        except Exception as e:
            print(e)
