import os
import socket
import time
def reg_cl(time_t, so_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
    client.connect(('localhost', 4345))  # 127.0.0.1
    client.send(time_t.encode())
    time.sleep(0.1)
    client.send(so_id.encode())



    client.close()