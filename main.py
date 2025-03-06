import os
import signal
import sys

from ascii_renderer.app import App

if __name__ == '__main__':
    # Clear terminal and hide cursor
    os.system('cls||clear')
    sys.stdout.write("\033[?25l")

    thread = App()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    thread.start()
    thread.join()
