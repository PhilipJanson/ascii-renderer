from __future__ import annotations
import math
from typing import Iterator

class Vec2:
    ZERO_VEC: Vec2 = None

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: Vec2) -> bool:
        return (self.x, self.y) == (other.x, other.y)

    def __iter__(self) -> Iterator[float]:
        return (self.x, self.y).__iter__()

    def __repr__(self) -> str:
        return f"X: {self.x:.2f}, Y: {self.y:.2f}"

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

class Vec3:
    ZERO_VEC: Vec3 = None

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __eq__(self, other: Vec3) -> bool:
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __iter__(self) -> Iterator[float]:
        return (self.x, self.y, self.z).__iter__()

    def __repr__(self) -> str:
        return f"X: {self.x:.2f}, Y: {self.y:.2f}, Z: {self.z:.2f}"

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, scalar: float) -> Vec3:
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def dot_product(self, other: Vec3) -> float:
        return sum(a * b for a, b in zip((self.x, self.y, self.z), (other.x, other.y, other.z)))

    def cross_product(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def scale(self, scalar: float) -> Vec3:
        return Vec3(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar
        )

    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def normalize(self) -> Vec3:
        length = self.length()
        if length == 0:
            return Vec3.ZERO_VEC
        return Vec3(self.x / length, self.y / length, self.z / length)

    def to_vec2(self, focal_length: float) -> Vec2:
        x = round(-focal_length * self.x / (-focal_length + self.z))
        y = round(-focal_length * self.y / (-focal_length + self.z))

        return Vec2(x, y)

class Axis:
    X = 'X'
    Y = 'Y'
    Z = 'Z'

class Direction:
    NORTH: Direction = None
    SOUTH: Direction = None
    EAST: Direction = None
    WEST: Direction = None
    UP: Direction = None
    DOWN: Direction = None

    def __init__(self, name: str, axis: str, vector: Vec3) -> None:
        self.name: str = name
        self.axis: str = axis
        self.vector: Vec3 = vector

class Face:
    def __init__(self, *vertices: Vec3, direction: Direction=None) -> None:
        self.vertex_count = len(vertices)
        self.vertices: list[Vec3] = list(vertices)
        self.direction: Direction = direction

        if self.vertex_count < 3:
            raise ValueError("A Face takes a minimum of three vertices.")

    def center(self) -> Vec3:
        return sum(self.vertices, Vec3.ZERO_VEC) / len(self.vertices)

    def normal(self) -> Vec3:
        edge1 = self.vertices[1] - self.vertices[0]
        edge2 = self.vertices[2] - self.vertices[0]
        return edge1.cross_product(edge2).normalize()

    def is_visible(self, camera_position: Vec3) -> tuple[bool, Vec3]:
        normal = self.normal()
        line_of_sight = camera_position - self.center()
        dot_product = normal.dot_product(line_of_sight)
        return dot_product >= 0, normal

    def get_edges(self) -> set[tuple[Vec3, Vec3]]:
        edges = set()
        for i in range(self.vertex_count):
            edge = (self.vertices[i], self.vertices[(i + 1) % self.vertex_count])
            edges.add(edge)
        return edges

class Shape:
    def __init__(self, center: Vec3, size: float) -> None:
        self.center = center
        self.size = size
        self.vertices: list[Vec3] = []
        self.edges: set[tuple[Vec3, Vec3]] = set()
        self.faces: list[Face] = []

    def rotate_x(self, theta: float) -> None:
        for vertex in self.vertices:
            new_y = vertex.y * math.cos(-theta) - vertex.z * math.sin(-theta)
            new_z = vertex.y * math.sin(-theta) + vertex.z * math.cos(-theta)

            vertex.y = new_y
            vertex.z = new_z

    def rotate_y(self, theta: float) -> None:
        for vertex in self.vertices:
            new_x = vertex.x * math.cos(theta) - vertex.z * math.sin(theta)
            new_z = vertex.x * math.sin(theta) + vertex.z * math.cos(theta)

            vertex.x = new_x
            vertex.z = new_z

    def rotate_z(self, theta: float) -> None:
        for vertex in self.vertices:
            new_x = vertex.x * math.cos(-theta) - vertex.y * math.sin(-theta)
            new_y = vertex.x * math.sin(-theta) + vertex.y * math.cos(-theta)

            vertex.x = new_x
            vertex.y = new_y

    def scale(self, factor: float) -> None:
        for vertex in self.vertices:
            vertex.scale(factor)

class Cube(Shape):
    def __init__(self, center: Vec3, size: float) -> None:
        super().__init__(center, size)
        half_size = size / 2

        vertices = [
            Vec3(center.x - half_size, center.y - half_size, center.z + half_size),
            Vec3(center.x + half_size, center.y - half_size, center.z + half_size),
            Vec3(center.x + half_size, center.y + half_size, center.z + half_size),
            Vec3(center.x - half_size, center.y + half_size, center.z + half_size),
            Vec3(center.x - half_size, center.y - half_size, center.z - half_size),
            Vec3(center.x + half_size, center.y - half_size, center.z - half_size),
            Vec3(center.x + half_size, center.y + half_size, center.z - half_size),
            Vec3(center.x - half_size, center.y + half_size, center.z - half_size)
        ]

        faces = [
            Face(vertices[0], vertices[1], vertices[2], vertices[3], direction=Direction.SOUTH),
            Face(vertices[7], vertices[6], vertices[5], vertices[4], direction=Direction.NORTH),
            Face(vertices[4], vertices[5], vertices[1], vertices[0], direction=Direction.UP),
            Face(vertices[6], vertices[7], vertices[3], vertices[2], direction=Direction.DOWN),
            Face(vertices[0], vertices[3], vertices[7], vertices[4], direction=Direction.EAST),
            Face(vertices[5], vertices[6], vertices[2], vertices[1], direction=Direction.WEST)
        ]

        self.vertices = vertices
        self.faces = faces

Vec2.ZERO_VEC = Vec2(0, 0)
Vec3.ZERO_VEC = Vec3(0, 0, 0)

Direction.NORTH = Direction('North', Axis.Z, Vec3(0, 0, -1))
Direction.SOUTH = Direction('South', Axis.Z, Vec3(0, 0, 1))
Direction.EAST = Direction('East', Axis.X, Vec3(1, 0, 0))
Direction.WEST = Direction('West', Axis.X, Vec3(-1, 0, 0))
Direction.UP = Direction('Up', Axis.Y, Vec3(0, -1, 0))
Direction.DOWN = Direction('Down', Axis.Y, Vec3(0, 1, 0))
