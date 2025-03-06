import threading
import time

from .geometry import Cube, Shape, Vec3
from .grid import Grid
from .renderer import Renderer

WIDTH = 30
HEIGHT = 30

class App(threading.Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.grid: Grid = Grid(WIDTH, HEIGHT)
        self.renderer: Renderer = Renderer(self.grid)
        self.grid.populate()

        self.shape: Shape = Cube(Vec3.ZERO_VEC, 10)

    def run(self) -> None:
        while True:
            self.grid.reset()
            self.shape.rotate_x(0.02)
            self.shape.rotate_y(0.02)
            self.shape.rotate_z(0.02)
            self.renderer.draw_shape(self.shape, debug=True)

            self.renderer.draw()
            time.sleep(0.02)
