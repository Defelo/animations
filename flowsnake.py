import random
from math import pi, cos, sin, atan, sqrt, acos

import pygame

from animations import Animation
from turtle import Turtle

COLORS = [
    0xFF0000,
    0xFFFF00,
    0x008800,
    0x00FFFF,
    0x0000FF,
]
BACKGROUND = (17, 17, 17)

WIDTH, HEIGHT = 600, 600

RECORD = False
FPS = 30
SECONDS = 7
FRAMES = FPS * SECONDS


def get_color(t):
    k = int(t * (len(COLORS) - 1))
    color1 = [COLORS[k] >> j & 0xFF for j in range(16, -1, -8)]
    color2 = [COLORS[min(k + 1, len(COLORS) - 1)] >> j & 0xFF for j in range(16, -1, -8)]
    t -= k / (len(COLORS) - 1)
    t *= len(COLORS) - 1
    return [round(color1[j] * (1 - t) + color2[j] * t) for j in range(3)]


class FlowSnake(Animation):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "flowsnake", FPS, RECORD)

        self.order = 7
        self.lines = []
        self.calculate()

    def calculate(self):
        points = [(0, 0)]

        def draw_line(_, b):
            points.append(b)

        turtle = Turtle(0, 0, 0, draw_line)
        self.draw_flowsnake(turtle, self.order, True, 1)

        padding = 50

        dx = points[-1][0] - points[0][0]
        dy = points[-1][1] - points[0][1]
        angle = -atan(dy / dx) - acos(5 / 2 / sqrt(7))
        if points[0][0] > points[-1][0]:
            angle += pi

        minx = 1e1337
        maxx = -1e1337
        miny = 1e1337
        maxy = -1e1337
        for i, (x, y) in enumerate(points):
            x, y = x * cos(angle) - y * sin(angle), x * sin(angle) + y * cos(angle)
            points[i] = x, y
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)

        last = None
        lines = []
        for i, (x, y) in enumerate(points):
            x = (x - minx) / (maxx - minx) * (self.width - padding * 2) + padding
            y = (y - miny) / (maxy - miny) * (self.height - padding * 2) + padding
            if last:
                t = (i - 1) / (len(points) - 1)
                lines.append((last, (x, y), t))
            last = x, y

        self.lines = lines

    def render(self):
        k = 100_000
        lines = [line for _, line in sorted([(i + random.randint(-k, k), line) for i, line in enumerate(self.lines)])]

        self.win.fill(BACKGROUND)

        for a, b, t in lines:
            pygame.draw.line(self.win, get_color(t), a, b)

        for _ in range(FPS // 2):
            yield

        head = 0
        tail = -len(lines) // 3
        cnt = 0
        total = (len(lines) - tail) // FRAMES
        while tail < len(lines):

            if head < len(lines):
                a, b, _ = lines[head]
                pygame.draw.line(self.win, (24, 24, 24), a, b)

            if tail >= 0:
                a, b, t = lines[tail]
                pygame.draw.line(self.win, get_color(t), a, b)

            head += 1
            tail += 1

            cnt += 1
            if cnt % total == 0:
                yield

    def draw_flowsnake(self, turtle: Turtle, order: int, axiom: bool, length: float):
        if not order:
            turtle.forward(length)
            return

        for k in "A-B--B+A++AA+B-" if axiom else "+A-BB--B-A++A+B":
            if k == "A":
                self.draw_flowsnake(turtle, order - 1, True, length)
            elif k == "B":
                self.draw_flowsnake(turtle, order - 1, False, length)
            elif k == "+":
                turtle.turn(-60)
            elif k == "-":
                turtle.turn(60)


animation = FlowSnake()
animation.run()
