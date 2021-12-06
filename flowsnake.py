import os
import random
import shutil
from math import pi, cos, sin, atan, sqrt, acos
from pathlib import Path

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

CREATE_GIF = 1

frame_dir = Path(__file__).parent / "frames"
if CREATE_GIF:
    if frame_dir.exists():
        shutil.rmtree(frame_dir)
    frame_dir.mkdir()

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
    def __init__(self, width: int, height: int):
        super().__init__(width, height, "FlowSnake")

        self.order = 7
        self.lines = []
        self.calculate()
        self._frame = 0

    def handle_key_down(self, key: int):
        if key in [pygame.K_q, pygame.K_ESCAPE]:
            pygame.quit()
        # elif key == pygame.K_LEFT and self.order > 1:
        #     self.order -= 1
        #     self.reduce()
        #     self.render()
        # elif key == pygame.K_RIGHT:
        #     self.order += 1
        #     self.render()
        elif key == pygame.K_r:
            self.render()

    def update(self):
        pass

    def calculate(self):
        points = [(0, 0)]

        def draw_line(_, b):
            points.append(b)

        turtle = Turtle(0, 0, 0, draw_line)
        self.draw_flowsnake(turtle, self.order, True, 1)

        padding = 50

        dx = points[-1][0] - points[0][0]
        dy = points[-1][1] - points[0][1]
        angle = -atan(dy / dx) - acos(5/2/sqrt(7))
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

        # k = 4096
        # badges = [lines[i * len(lines) // k : (i + 1) * len(lines) // k] for i in range(k)]
        # lines = []
        # # random.shuffle(badges)
        # # for badge in badges:
        # #     lines.extend(badge)
        # for badge in map(list, zip(*badges)):
        #     random.shuffle(badge)
        #     lines.extend(badge)

        # random.shuffle(lines)

        # a = lines[:len(lines)//2][::-1]
        # b = lines[len(lines)//2:]
        # lines = []
        # for x, y in zip(a, b):
        #     lines.extend([x, y])

        # k = 7 ** 4
        # parts = [lines[i * len(lines) // k:(i + 1) * len(lines) // k] for i in range(k)]
        # parts = [
        #     [k
        #      for x, y in zip(p[:len(p) // 2][::-1], p[len(p) // 2:])
        #      for k in [x, y]]
        #     for p in parts
        # ]
        # lines = []
        # for parts in zip(*parts):
        #     lines.extend(parts)

    def reduce(self):
        lines = []
        for i in range(0, len(self.lines), 7):
            lines.append((self.lines[i][0], self.lines[i+6][1], (self.lines[i][2] + self.lines[i+6][2]) / 2))
        self.lines = lines

    def frame(self, d=1):
        if CREATE_GIF:
            pygame.image.save(self.win, f"{frame_dir}/frame_{self._frame:06d}.png")

        self._frame += d
        pygame.display.update()
        pygame.time.delay(1000 // FPS)

    def render(self):
        # start = True
        # dr = 0.02
        # # self._frame = 999999
        # while self.order >= 2:
        #     r = 0
        #     while r <= 1:
        #         self.win.fill(BACKGROUND)
        #
        #         for i, (a, b, t) in enumerate(self.lines):
        #             rla = self.lines[i - (i % 7)][0]
        #             rlb = self.lines[i + 6 - (i % 7)][1]
        #             ra = tuple((rla[k] * (7 - i % 7) + rlb[k] * (i % 7)) / 7 for k in range(2))
        #             rb = tuple((rla[k] * (6 - i % 7) + rlb[k] * (1 + i % 7)) / 7 for k in range(2))
        #             # pygame.draw.line(self.win, (128, 128, 128), a, b)
        #             a = tuple(round(r * ra[k] + (1-r) * a[k]) for k in range(2))
        #             b = tuple(round(r * rb[k] + (1-r) * b[k]) for k in range(2))
        #             pygame.draw.line(self.win, get_color(t), a, b, width=max(1, min(2, 5 - self.order)))
        #             # pygame.draw.line(self.win, (255, 255, 255), ra, rb)
        #
        #         for _ in range(FPS // (2 if start else 5) if r == 0 else 1):
        #             if start:
        #                 self.frame()
        #                 self._frame = 999999
        #                 start = False
        #             else:
        #                 self.frame(-1)
        #         r += dr
        #
        #     self.reduce()
        #     self.order -= 1
        #     # dr /= 1.5
        #     # dr /= sqrt(7)
        #
        # if CREATE_GIF:
        #     os.system(f"convert -delay {100 / FPS:.3} -loop 0 {frame_dir}/frame_*.png flowsnake.gif")
        #     pygame.quit()
        #
        # return

        # lines = []
        # pending = []
        # for line in self.lines:
        #     pending.append(line)
        #     if len(pending) > len(self.lines) // 15:
        #         i = random.randrange(len(pending))
        #         lines.append(pending.pop(i))
        # random.shuffle(pending)
        # lines += pending
        k = 100_000
        lines = [line for _, line in sorted([(i + random.randint(-k, k), line) for i, line in enumerate(self.lines)])]

        # self.win.fill(BACKGROUND)
        # for a, b, t in lines:
        #     # t = (i - 1) / len(self.lines)
        #     pygame.draw.line(self.win, get_color(t), a, b)

        # head = 0
        # tail = -100_000
        # while tail < len(lines):
        #
        #     head += 1
        #     tail += 1

        self.win.fill(BACKGROUND)

        for a, b, t in lines:
            pygame.draw.line(self.win, get_color(t), a, b)

        for _ in range(FPS // 2):
            self.frame()

        head = 0
        tail = -len(lines)//3
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
                self.frame()

        # cnt = 0
        # frame = 2000
        # for a, b, t in lines:
        #     # t = (i - 1) / len(self.lines)
        #     pygame.draw.line(self.win, get_color(t), a, b)
        #     cnt += 1
        #     if cnt % (len(lines) // FRAMES) == 0:
        #         pygame.display.update()
        #         if CREATE_GIF:
        #             pygame.image.save(self.win, f"{frame_dir}/frame_{frame:06d}.png")
        #         frame += 1
        #         pygame.time.delay(1000 // FPS)
        #
        # for _ in range(FPS // 2):
        #     if CREATE_GIF:
        #         pygame.image.save(self.win, f"{frame_dir}/frame_{frame:06d}.png")
        #     frame += 1
        #
        # # self.win.fill(BACKGROUND)
        # # lines = [line for _, line in sorted([(i + random.randint(-k, k), line) for i, line in enumerate(self.lines)])]
        # cnt = 0
        # frame = 0
        # for a, b, t in lines:
        #     if cnt % (len(lines) // FRAMES) == 0:
        #         pygame.display.update()
        #         if CREATE_GIF:
        #             pygame.image.save(self.win, f"{frame_dir}/frame_{frame:06d}.png")
        #         frame += 1
        #         pygame.time.delay(1000 // FPS)
        #     cnt += 1
        #     # t = (i - 1) / len(self.lines)
        #     pygame.draw.line(self.win, BACKGROUND, a, b)

        # print(frame)

        if CREATE_GIF:
            # pygame.image.save(self.win, f"{frame_dir}/frame_{0:06d}.png")
            os.system(f"convert -delay {100 / FPS:.3} -loop 0 {frame_dir}/frame_*.png flowsnake.gif")
            pygame.quit()

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


animation = FlowSnake(600, 600)
animation.run()
