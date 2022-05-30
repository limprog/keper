def readf():
    f = open('consig.txt','r')
    data = f.read()
    if data =='':
        scr = 100
        tscr = 60
        var = 0
        cod = 1234
    else:
        scr, tscr, var, cod = list(map(int, f.readlines()))
    f.close()
    return scr, tscr, var, cod

def writef(sve, scr, tscr, var, cod):
    if sve == 1:
        f = open('consig.txt', 'w')
        f.write(str(scr)+'\n'+str(tscr)+'\n'+str(var)+'\n'+str(cod))
    else:
        pass