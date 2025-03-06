import threading
import time

class App(threading.Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)

    def run(self) -> None:
        time.sleep(0.02)
