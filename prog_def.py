import os
import random

from constants import *
def check(prg, list, cod2, ren,der, renr):
    if prg == cod2:
        prog = 1
        if list == 1:
            list_print(der=der)
        if ren == 1:
            rename(der=der)
        if renr == 1:
            renamerandoom(der)
    else:
        prog = 0
    return prog,


def list_print(der):
    fils = os.listdir(f'Screenshoot\{der}')
    print(' '.join(fils))


def rename(der):
    fils = os.listdir(f'Screenshoot\{der}')
    for i in range(len(fils)):
        name = '{0}.png'.format(i+1)
        os.rename(os.path.join(f'Screenshoot\{der}',fils[i]), os.path.join(f'Screenshoot\{der}', name))

def renamerandoom(der):
    fils = os.listdir(f'Screenshoot\{der}')
    for i in range(len(fils)):
        name = '{0}.png'.format(random.randint(10000, 1000000000))
        os.rename(os.path.join(f'Screenshoot\{der}',fils[i]), os.path.join(f'Screenshoot\{der}', name))
def codes(cod,cod2):
    cod = cod2
    return cod