import sys

from .color import *
from .geometry import Direction, Face, Shape, Vec2, Vec3
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
            is_visible, normal = face.is_visible(CAMERA_POSITION)

            # Backface culling
            if is_visible:
                self.rasterize_face(face)
                self.draw_face(face, color=BRIGHT_GREEN)

            if debug:
                color = self.get_color_from_direction(face.direction)
                self.draw_normal(normal.scale(12), color=color)

    def draw_wireframe(self, shape: Shape, debug=False) -> None:
        for face in shape.faces:
            self.draw_face(face, color=RED)

            if debug:
                color = self.get_color_from_direction(face.direction)
                self.draw_normal(face.normal().normalize().scale(12), color=color)

    def draw_face(self, face: Face, color: str=None) -> None:
        for edge in face.get_edges():
            startVec = edge[0].to_vec2(FOCAL_LENGTH)
            endVec = edge[1].to_vec2(FOCAL_LENGTH)
            self.draw_line(startVec, endVec, color=color)

    def draw_normal(self, normal: Vec3, color: str=None) -> None:
        self.draw_line(Vec2.ZERO_VEC, normal.to_vec2(100), color=color)

    def draw_line(self, start_vec: Vec2, end_vec: Vec2, color: str=None) -> None:
        delta_x = abs(end_vec.x - start_vec.x)
        delta_y = abs(end_vec.y - start_vec.y)
        step_x = 1 if start_vec.x < end_vec.x else -1
        step_y = 1 if start_vec.y < end_vec.y else -1
        err = delta_x - delta_y
        curr_x = start_vec.x
        curr_y = start_vec.y

        while True:
            pixel = self._grid.get_pixel(curr_x, curr_y)
            if pixel:
                pixel.char = self.get_char_for_line(delta_x, delta_y, curr_x, curr_y, end_vec)
                if color:
                    pixel.color = color

            if curr_x == end_vec.x and curr_y == end_vec.y:
                break

            double_err = 2 * err
            if double_err > -delta_y:
                err -= delta_y
                curr_x += step_x
            if double_err < delta_x:
                err += delta_x
                curr_y += step_y

    def rasterize_face(self, face: Face) -> None:
        edges, min_y, max_y = face.get_2d_edges(FOCAL_LENGTH)
        edges.sort(key=lambda edge: edge[0].y)

        active_edges: list[tuple[Vec2, Vec2]] = []
        y = min_y
        while y <= max_y:
            while edges and edges[0][0].y == y:
                active_edges.append(edges.pop(0))

            active_edges = [edge for edge in active_edges if edge[1].y != y]

            active_edges.sort(key=lambda edge: edge[0].x + (y - edge[0].y)
                                                         * (edge[1].x - edge[0].x)
                                                         / (edge[1].y - edge[0].y))

            for i in range(0, len(active_edges), 2):
                if i + 1 >= len(active_edges):
                    break

                active_edge1: tuple[Vec2, Vec2] = active_edges[i]
                x_start = int(active_edge1[0].x + (y - active_edge1[0].y)
                                                * (active_edge1[1].x - active_edge1[0].x)
                                                / (active_edge1[1].y - active_edge1[0].y))

                active_edge2: tuple[Vec2, Vec2] = active_edges[i + 1]
                x_end = int(active_edge2[0].x + (y - active_edge2[0].y)
                                              * (active_edge2[1].x - active_edge2[0].x)
                                              / (active_edge2[1].y - active_edge2[0].y))
                for x in range(x_start, x_end + 1):
                    pixel = self._grid.get_pixel(x, y)
                    if pixel:
                        pixel.char = '#'
                        pixel.color = LIGHT_GRAY

            y += 1

    def get_char_for_line(self, delta_x: float, delta_y: float, curr_x: float, curr_y: float,
                          end_vec: Vec2) -> str:
        if curr_x == end_vec.x and curr_y == end_vec.y:
            return '+'
        # Check if end_vec.x is equal to curr_x to avoid division by zero
        if delta_x < 4 or end_vec.x == curr_x:
            return '|'
        if delta_y < 4:
            return '_'
        k = (end_vec.y - curr_y) / (end_vec.x - curr_x)
        return '/' if k < 0 else '\\'

    def get_color_from_direction(self, direction: Direction) -> str:
        if direction == Direction.NORTH:
            return BRIGHT_RED
        elif direction == Direction.SOUTH:
            return BRIGHT_YELLOW
        elif direction == Direction.EAST:
            return BRIGHT_BLUE
        elif direction == Direction.WEST:
            return BRIGHT_MAGENTA
        elif direction == Direction.UP:
            return BRIGHT_CYAN
        else:
            return WHITE

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
