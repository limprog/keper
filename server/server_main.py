from server_img import *
from server_reg import *

from threading import Thread

th_1, th_2 = Thread(target=reg), Thread(target = img)

if __name__ == '__main__':
    th_1.start(), th_2.start()
    th_1.join(), th_2.join()
