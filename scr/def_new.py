


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




