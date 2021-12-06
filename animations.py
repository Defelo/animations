import os
import shutil
from pathlib import Path

import pygame

frame_dir = Path(__file__).parent / "frames"


class Animation:
    def __init__(self, width: int, height: int, name: str, fps: int, record: bool):
        self.width = width
        self.height = height
        self.name = name
        self.win = None
        self.record = record
        self._frame = 0
        self.fps = fps

    def init(self):
        if self.record:
            if frame_dir.exists():
                shutil.rmtree(frame_dir)
            frame_dir.mkdir()

        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.name)

    def frame(self):
        if self.record:
            pygame.image.save(self.win, f"{frame_dir}/frame_{self._frame:06d}.png")

        self._frame += 1
        pygame.display.update()
        if not self.record:
            pygame.time.delay(1000 // self.fps)

    def render(self):
        yield

    def run(self):
        self.init()
        for _ in self.render():
            self.frame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    return

        if self.record:
            os.system(f"convert -delay {100 / self.fps:.3} -loop 0 {frame_dir}/frame_*.png {self.name}.gif")
            pygame.quit()
