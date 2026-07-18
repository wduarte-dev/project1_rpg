from os import name, system
from time import time
from sys import stdin, stdout


timeout = 1
if name == 'nt': 
    import msvcrt
    def get_key(): #type:ignore
        start_time = time()
        while time() - start_time < timeout:
            if msvcrt.kbhit(): #type:ignore
                return msvcrt.getch().decode('utf-8', errors='ignore').lower() #type:ignore
        return None 
else: 
    import tty, termios, select
    def get_key():
        fd = stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            rlist, _, _ = select.select([stdin], [], [], timeout)
            if rlist:
                ch = stdin.read(1)
            else:
                ch = None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.lower() if ch else None


def clear_terminal(mode):
        if mode == 0: # write in old
            stdout.write('\033[H')
            stdout.flush()
        elif mode == 1: # clear all
            system('cls' if name == 'nt' else 'clear')