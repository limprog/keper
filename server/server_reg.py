from datetime import datetime
import socket
import time

def reg():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
    server.bind(('localhost', 4345))  # 127.0.0.1
    server.listen()
    print("gydy")
    while True:
        client_socket, client_address = server.accept()
        time_t = client_socket.recv(1024).decode()
        so_id = client_socket.recv(1024).decode()
        print(time_t, so_id)

        client_socket.close()
