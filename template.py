import random

import pygame

from animations import Animation

BACKGROUND = (0, 0, 0)

WIDTH, HEIGHT = 600, 600

RECORD = False
FPS = 30


class Template(Animation):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "template", FPS, RECORD)

    def render(self):
        w, h = 20, 20
        x, y = random.randrange(self.width - w), random.randrange(self.height - h)
        dx = random.randrange(-5, 5)
        dy = random.randrange(-5, 5)
        while True:
            self.win.fill(BACKGROUND)
            pygame.draw.rect(self.win, (255, 255, 255), (x, y, w, h))
            if x + dx not in range(self.width - w):
                dx = -dx
            if y + dy not in range(self.height - h):
                dy = -dy
            x += dx
            y += dy
            yield


animation = Template()
animation.run()
