import pygame


class Animation:
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self.title = title
        self.win = None

    def init(self):
        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def update(self):
        pass

    def render(self):
        pass

    def handle_key_down(self, key: int):
        pass

    def handle_key_up(self, key: int):
        pass

    def loop(self):
        self.render()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_key_down(event.key)
                if event.type == pygame.KEYUP:
                    self.handle_key_up(event.key)
            self.update()
            pygame.display.update()
            pygame.time.delay(20)

    def run(self):
        self.init()
        self.loop()
