
import os
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('localhost', 4344))  # 127.0.0.1

file = open(os.path.join('../Screenshoot/data/HI.png'), 'rb')
image_data = file.read(2048)

while image_data:
    client.send(image_data)
    image_data = file.read(2048)

file.close()
client.close()