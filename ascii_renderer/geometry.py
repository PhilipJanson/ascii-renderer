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

class Face:
    def __init__(self, *vertices: Vec3) -> None:
        self.vertex_count = len(vertices)
        self.vertices: list[Vec3] = list(vertices)

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

Vec2.ZERO_VEC = Vec2(0, 0)
Vec3.ZERO_VEC = Vec3(0, 0, 0)
