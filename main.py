from screenshot import *
import argparse

if __name__ == '__main__':
    screenshot_maker = Screenshoot()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--scr', default=5, type=int, help='Number of screenshots')
    parser.add_argument('--tscr', default=10, type=int, help='time between screenshots')
    parser.add_argument('--var', default=0, type=int, help='scatter')
    args = parser.parse_args()
    min = args.tscr - args.var
    max = args.tscr + args.var
    for i in range(args.scr):
        screenshot_maker.screen()
        time.sleep(random.randint(min, max))

