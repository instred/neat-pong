import pygame

class Paddle:
    velocity = 4
    width = 15
    height = 120

    def __init__(self, x: int, y: int) -> None:
        self.x = self.start_x = x
        self.y = self.start_y = y

    def draw(self, window: pygame.display) -> None:
        pygame.draw.rect(window, (255,255,255), (self.x, self.y, self.width, self.height))

    def move(self, up=True) -> None:
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def reset(self) -> None:
        self.x = self.start_x
        self.y = self.start_y