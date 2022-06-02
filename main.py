from screenshot import *
import argparse
from prog_def import *
import time
from def_new import *

if __name__ == '__main__':
    #f = open('consig.txt', 'w')
    #f.close()
    # scr, tscr, var, cod = readf()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--scr', default=100, type=int, help='Number of screenshots')
    parser.add_argument('--tscr', default=60, type=int, help='time between screenshots')
    parser.add_argument('--var', default=0, type=int, help='scatter')
    parser.add_argument('--prg', default=0, type=int)
    parser.add_argument('--cod', default=1234, type=int)
    parser.add_argument('--list', default=0, type=int, help='print all files in a folder')
    parser.add_argument('--ren', default=0, type=int, help='rename files by sequence')
    parser.add_argument('--sve', default=1, type=int, help='save arguments or not')
    parser.add_argument('--der', default=today, type=str)
    parser.add_argument('--renr', default=0, type=int)
    args = parser.parse_args()
    screenshot_maker = Screenshoot(der=args.der)
    writef(args.sve, args.scr, args.tscr, args.var, args.cod)
    min = args.tscr - args.var
    max = args.tscr + args.var
    prog = check(prg=args.prg, cod2=args.cod, list=args.list, ren=args.ren, der=args.der, renr=args.renr)
    writef(args.sve, args.scr, args.tscr, args.var, args.cod)
    if prog == 0:
        for i in range(args.scr):
            screenshot_maker.screen(args.der)
            time.sleep(random.randint(min, max))
    else:
        pass

