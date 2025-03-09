import os
import signal
import sys

from ascii_renderer.app import App

if __name__ == '__main__':
    # Clear terminal and hide cursor
    os.system('cls||clear')
    sys.stdout.write("\033[?25l")

    app = App()
    app.register_key_bindings()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.start()
    app.join()
