from server.client_reg import *


def readf():
    f = open('consig.txt','r')
    data = f.readline(1)
    if data =='':
        print(data)
        scr = 100
        tscr = 60
        var = 0
        cod = 1234
    else:
        scr, tscr, var, cod = list(map(int, f.readlines()))


    f.close()
    return scr, tscr, var, cod

def writef(sve, *params):
    if sve == 1:
        f = open('consig.txt', 'w')
        f.writelines("\n".join(list(map(str, params))))

    else:
        pass


def reg(reg):
    if reg == 1:
        time_1 = input("когда начало\n>>>")
        time_2 = input("дни недели (англ сокращение)\n>>>").upper()
        time_t = time_1, time_2
        so_id = input("id кружка")
        with open("comp.txt", access_mode="w") as f:
            f.write(time_t)
        reg_cl(time_t,so_id)

