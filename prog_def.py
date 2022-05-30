import os
from constants import *
def check(prg, list, cod, ren,der):
    if prg == cod:
        prog = 1
        if list == 1:
            list_print(der=der)
        if ren == 1:
            rename(der=der)
    else:
        prog = 0
    return prog


def list_print(der):
    fils = os.listdir(f'Screenshoot\{der}')
    print(' '.join(fils))


def rename(der):
    fils = os.listdir(f'Screenshoot\{der}')
    for i in range(len(fils)):
        name = '{0}.png'.format(i+1)
        os.rename(os.path.join(f'Screenshoot\{der}',fils[i]), os.path.join(f'Screenshoot\{der}', name))