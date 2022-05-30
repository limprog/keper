import os
from constants import *
def check(prg, list, cod, ren):
    if prg == cod:
        prog = 1
        if list == 1:
            list_print()
        if ren == 1:
            rename()
    else:
        prog = 0
    return prog


def list_print():
    fils = os.listdir(f'Screenshoot\{today}')
    print(' '.join(fils))


def rename():
    fils = os.listdir(f'Screenshoot\{today}')
    for i in range(len(fils)):
        name = '{0}.png'.format(i+1)
        os.rename(os.path.join(f'Screenshoot\{today}',fils[i]), os.path.join(f'Screenshoot\{today}', name))