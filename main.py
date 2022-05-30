from screenshot import *
import argparse
from prog_def import *
import time
from def_new import *

if __name__ == '__main__':
    f = open('consig.txt', 'w')
    screenshot_maker = Screenshoot()
    scr, tscr, var, cod = readf()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--scr', default=scr, type=int, help='Number of screenshots')
    parser.add_argument('--tscr', default=tscr, type=int, help='time between screenshots')
    parser.add_argument('--var', default=var, type=int, help='scatter')
    parser.add_argument('--prg', default=0, type=int)
    parser.add_argument('--cod', default=cod, type=int)
    parser.add_argument('--list', default=0, type=int, help='print all files in a folder')
    parser.add_argument('--ren', default=0, type=int, help='rename files by sequence')
    parser.add_argument('--sve', default=1, type=int, help='save arguments or not')
    args = parser.parse_args()
    writef(args.sve, args.scr, args.tscr, args.var, args.cod)
    min = args.tscr - args.var
    max = args.tscr + args.var
    prog = check(prg=args.prg, cod=args.cod, list=args.list, ren=args.ren)
    if prog != 1:
        for i in range(args.scr):
            screenshot_maker.screen()
            time.sleep(random.randint(min, max))

