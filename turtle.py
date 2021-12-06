from math import cos, sin, pi
from typing import Callable, Any


class Turtle:
    def __init__(
        self, x: float, y: float, angle: float, on_draw: Callable[[tuple[float, float], tuple[float, float]], Any]
    ):
        self.x = x
        self.y = y
        self.angle = angle
        self.on_draw = on_draw

    def forward(self, distance):
        dx, dy = cos(self.angle / 180 * pi) * distance, -sin(self.angle / 180 * pi) * distance
        self.x += dx
        self.y += dy
        self.on_draw((self.x - dx, self.y - dy), (self.x, self.y))

    def turn(self, angle):
        self.angle += angle
