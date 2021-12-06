from math import pi

import pygame

from animations import Animation, rotate

BACKGROUND = (24, 25, 28)
GREEN1 = (178, 229, 203)
GREEN2 = (102, 204, 152)
GREEN3 = (50, 153, 101)

SIZE = 512
PADDING = 2 / 21


RECORD = True
FPS = 60


class PyDrocsid(Animation):
    def __init__(self):
        super().__init__(SIZE, SIZE, "pydrocsid", FPS, RECORD)

    def render_frame(self, r):
        self.win.fill(BACKGROUND)

        size = SIZE / (1 + 2 * PADDING)
        padding = size * PADDING

        def draw_polygon(_color, *_points):
            pygame.draw.polygon(
                self.win,
                _color,
                [(round(padding + (x + 1) / 2 * size), round(padding + (y + 1) / 2 * size)) for x, y in _points],
            )

        for i in range(4):
            p1 = 0.5, 0
            p2 = 0, -0.5
            p3 = 0.5, -0.5
            orig = p1, p2, p3
            k = (r - 3) * 1
            if k > 0:
                p1 = p1[0] + k, p1[1] + k
                p2 = p2[0] + k, p2[1] + k
                p3 = p3[0] + k, p3[1] + k

            draw_polygon(
                GREEN3, *[rotate(*rotate(*p, min(0.5, max(0, r - i / 6)) * pi, *p1), i * pi / 2) for p in [p1, p2, p3]]
            )

            if k > 0:
                p1, p2, p3 = orig
                p1 = p1[0] - k, p1[1] + k
                p2 = p2[0] - k, p2[1] + k
                p3 = p3[0] - k, p3[1] + k

            draw_polygon(
                GREEN3, *[rotate(*rotate(*p, min(1, max(0, r - i / 6)) * pi, *p1), i * pi / 2) for p in [p1, p2, p3]]
            )

            if r - i / 6 < 1:
                continue

            k = max(0, min(1, (r - i / 6 - 1) * 2))
            p1 = 0.5, 0.5
            p2 = 1, 0.5
            p3 = 1, 0.5 + k * 0.25

            if r > 3:
                k = (r - 3) * 1
                p1 = p1[0] + k, p1[1] + k
                p2 = p2[0] + k, p2[1] + k
                p3 = p3[0] + k, p3[1] + k

            draw_polygon(GREEN1, *[rotate(*p, i * pi / 2) for p in [p1, p2, p3]])

        draw_polygon(GREEN2, (-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5))

        r -= 1.25
        if r < 0 or r > 2.2:
            return

        for i in range(4):
            p1 = 0.3, -0.3
            p2 = 0.3, -0.05
            p3 = 0.05, (p1[1] + p2[1]) / 2
            m = [sum(p[i] for p in [p1, p2, p3]) / 3 for i in range(2)]
            s = max(0, min(1, (r - i / 6) * 4))
            if r > 1.75:
                k = (r - 1.75) * 2
                p1 = p1[0] - k, p1[1]
                p2 = p2[0] - k, p2[1]
                p3 = p3[0] - k, p3[1]
            draw_polygon(
                BACKGROUND, *[rotate(*[p[k] * s + m[k] * (1 - s) for k in range(2)], -i * pi / 2) for p in [p1, p2, p3]]
            )

    def render(self):
        r = 2.75
        dr = 0.025

        while r < 4.5:
            self.render_frame(r)
            r += dr
            yield

        r = 0
        while r < 2:
            self.render_frame(r)
            r += dr
            yield

        for _ in range(self.fps // 2):
            yield


animation = PyDrocsid()
animation.run()
