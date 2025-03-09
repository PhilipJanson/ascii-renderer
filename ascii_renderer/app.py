import threading
import time

import keyboard
from .geometry import Cube, Shape, Vec3
from .grid import Grid
from .renderer import Renderer

WIDTH = 100
HEIGHT = 50
ROTATION_SPEED = 0.02

class App(threading.Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.grid: Grid = Grid(WIDTH, HEIGHT)
        self.renderer: Renderer = Renderer(self.grid)
        self.grid.populate()

        self.shape: Shape = Cube(Vec3.ZERO_VEC, 20)
        self.is_running: bool = True
        self.x_rotation: float = 0.0
        self.y_rotation: float = 0.0
        self.z_rotation: float = 0.0

    def run(self) -> None:
        while True:
            self.grid.reset()
            self.update()
            self.render()
            time.sleep(0.02)

    def update(self) -> None:
        if self.is_running:
            self.shape.rotate_x(self.x_rotation)
            self.shape.rotate_y(self.y_rotation)
            self.shape.rotate_z(self.z_rotation)

    def render(self) -> None:
        self.renderer.draw_shape(self.shape)
        self.renderer.draw()

    def pause(self) -> None:
        self.is_running = not self.is_running

    def set_x_rotation(self, theta: float) -> None:
        if self.x_rotation == 0:
            self.x_rotation = theta
        elif self.x_rotation + theta == 0:
            self.x_rotation = 0

    def set_y_rotation(self, theta: float) -> None:
        if self.y_rotation == 0:
            self.y_rotation = theta
        elif self.y_rotation + theta == 0:
            self.y_rotation = 0

    def set_z_rotation(self, theta: float) -> None:
        if self.z_rotation == 0:
            self.z_rotation = theta
        elif self.z_rotation + theta == 0:
            self.z_rotation = 0

    def register_key_bindings(self) -> None:
        keyboard.add_hotkey('space', self.pause)
        keyboard.add_hotkey('w', lambda: self.set_x_rotation(ROTATION_SPEED))
        keyboard.add_hotkey('s', lambda: self.set_x_rotation(-ROTATION_SPEED))
        keyboard.add_hotkey('a', lambda: self.set_y_rotation(ROTATION_SPEED))
        keyboard.add_hotkey('d', lambda: self.set_y_rotation(-ROTATION_SPEED))
        keyboard.add_hotkey('q', lambda: self.set_z_rotation(ROTATION_SPEED))
        keyboard.add_hotkey('e', lambda: self.set_z_rotation(-ROTATION_SPEED))
