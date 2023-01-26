
from datetime import datetime
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
server.bind(('localhost', 4344))  # 127.0.0.1
server.listen()

client_socket, client_address = server.accept()
now = datetime.now()
now_time = str(now.strftime("%H.%M.%S"))

file = open(f"{now_time}.png", "wb")
image_chunk = client_socket.recv(2048)  # stream-based protocol

while image_chunk:
    file.write(image_chunk)
    image_chunk = client_socket.recv(2048)

file.close()
client_socket.close()