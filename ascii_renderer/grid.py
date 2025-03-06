from __future__ import annotations
from typing import Optional
from .color import END

PIXEL_CHAR = ' '

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid_width: int = width // 2
        self.grid_height: int = height // 2
        self._grid: dict[tuple[int, int], Pixel] = {}

    def reset(self) -> None:
        for pixel in self._grid.values():
            pixel.char = PIXEL_CHAR

    def populate(self) -> None:
        for y in range(-self.grid_height, self.grid_height):
            for x in range(-self.grid_width, self.grid_width):
                self._grid[(x, y)] = Pixel(PIXEL_CHAR)

    def get_pixel(self, x: int, y: int) -> Optional[Pixel]:
        return self._grid.get((x, y))

class Pixel():
    def __init__(self, char: str, color: str=None) -> None:
        self.char: str = char
        self.color: str = color

    def __str__(self) -> str:
        return self.char if self.color is None else f'{self.color}{self.char}{END}'
