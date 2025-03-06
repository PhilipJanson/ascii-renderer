import sys

from .color import BRIGHT_GREEN, RED
from .geometry import Face, Shape, Vec2, Vec3
from .grid import Grid

SPACER_CHAR = ' '
CAMERA_POSITION = Vec3(0, 0, 100)
FOCAL_LENGTH = 100.0

class Renderer:
    def __init__(self, grid: Grid) -> None:
        self._grid: Grid = grid
        self._previous_frame: str = ''

    def draw_shape(self, shape: Shape, debug: bool=False) -> None:
        for face in shape.faces:
            # Backface culling
            is_visible, normal = face.is_visible(CAMERA_POSITION)

            if is_visible:
                self.draw_face(face, color=BRIGHT_GREEN)

                if debug:
                    self.draw_normal(normal.scale(10), color=RED)

    def draw_wireframe(self, shape: Shape) -> None:
        for face in shape.faces:
            self.draw_face(face, color=RED)

    def draw_face(self, face: Face, color: str=None) -> None:
        for edge in face.get_edges():
            startVec = edge[0].to_vec2(FOCAL_LENGTH)
            endVec = edge[1].to_vec2(FOCAL_LENGTH)
            self.draw_vector(startVec, endVec, color=color)

    def draw_normal(self, normal: Vec3, color: str=None) -> None:
        self.draw_vector(Vec2.ZERO_VEC, normal.to_vec2(100), color=color)

    def draw_vector(self, a: Vec2, b: Vec2, color: str=None) -> None:
        self.draw_line(a.x, a.y, b.x, b.y, color=color)

    def draw_line(self,
                  start_x: int,
                  start_y: int,
                  end_x: int,
                  end_y: int,
                  color: str=None) -> None:
        delta_x = abs(end_x - start_x)
        delta_y = abs(end_y - start_y)
        sx = 1 if start_x < end_x else -1
        sy = 1 if start_y < end_y else -1
        err = delta_x - delta_y
        curr_x = start_x
        curr_y = start_y

        while True:
            pixel = self._grid.get_pixel(curr_x, curr_y)
            if pixel:
                char = self.get_char_from_line(start_x, start_y, end_x, end_y, curr_x, curr_y)
                pixel.char = char
                if color:
                    pixel.color = color

            if curr_x == end_x and curr_y == end_y:
                break

            e2 = 2 * err

            if e2 > -delta_y:
                err = err - delta_y
                curr_x = curr_x + sx

            if e2 < delta_x:
                err = err + delta_x
                curr_y = curr_y + sy

    def get_char_from_line(self,
                           start_x: int,
                           start_y: int,
                           end_x: int,
                           end_y: int,
                           curr_x: int,
                           curr_y: int) -> str:
        if (start_x, start_y) == (curr_x, curr_y) or (end_x, end_y) == (curr_x, curr_y):
            return '+'

        delta_x = end_x - start_x
        delta_y = end_y - start_y

        if abs(delta_x) < 2:
            return '|'
        if abs(delta_y) < 2:
            return '_'

        k = delta_y / delta_x
        return '/' if k < 0 else '\\'

    def draw(self) -> None:
        buffer = []

        for y in range(-self._grid.grid_height, self._grid.grid_height):
            row = []
            for x in range(-self._grid.grid_width, self._grid.grid_width):
                row.append(str(self._grid.get_pixel(x, y)))
            buffer.append(SPACER_CHAR.join(row))

        new_frame = '\n'.join(buffer)

        if new_frame != self._previous_frame:
            sys.stdout.write('\n' + new_frame)
            sys.stdout.write(f'\033[{self._grid.height}A')
            sys.stdout.flush()
            self._previous_frame = new_frame
