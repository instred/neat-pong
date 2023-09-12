import pygame
import math
from random import random

class Ball:
    velocity = 5
    radius = 8


    def __init__(self, x : int, y: int) -> None:
        self.x = self.start_x = x
        self.y = self.start_y = y



    def draw(self, window : pygame.display) -> None:
        pygame.draw.circle(window, (255,255,255), (self.x, self.y), self.radius)

    def move(self) -> None:
        pass

    def reset(self) -> None:
        self.x = self.start_x
        self.y = self.start_y