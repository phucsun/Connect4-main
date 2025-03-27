import socket

class ConnectFourClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host= '10.10.75.13' , port=12345):
        try:
            self.client_socket.connect((host, port))
            print(f"Đã kết nối tới server {host}:{port}")
        except ConnectionRefusedError:
            print("Không thể kết nối tới server. Vui lòng thử lại sau.")
            exit(1)

    def send_move(self, move):
        """Gửi nước đi của AI lên server"""
        try:
            self.client_socket.send(str(move).encode('utf-8'))
        except BrokenPipeError:
            print("Mất kết nối tới server.")
            exit(1)

    def get_move(self):
        """Nhận nước đi từ server"""
        try:
            move = self.client_socket.recv(1024).decode('utf-8')
            return int(move)
        except ValueError:
            print("Dữ liệu nhận được từ server không hợp lệ.")
            return -1  # Trả về giá trị lỗi để xử lý tiếp

    def close(self):
        """Đóng kết nối khi game kết thúc"""
        self.client_socket.close()