import pygame
import math
from random import random, randrange

class Ball:
    velocity = 8
    radius = 10


    def __init__(self, x : int, y: int) -> None:
        self.x = self.start_x = x
        self.y = self.start_y = y

        angle : float = self.getAngle(-30,30)
        start_pos : int = 1 if random() < 0.5 else - 1

        self.x_velocity = start_pos * abs(math.cos(angle) * self.velocity)
        self.y_velocity = math.sin(angle) * self.velocity


    def getAngle(self, min_angle, max_angle, excluded=[0]) -> float:
        angle = 0
        while angle in excluded:
            angle = math.radians(randrange(min_angle, max_angle))

        return angle


    def draw(self, window : pygame.display) -> None:
        pygame.draw.circle(window, (255,255,255), (self.x, self.y), self.radius)

    def move(self) -> None:
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self) -> None:
        self.x = self.start_x
        self.y = self.start_y

        angle = self.getAngle(-30,30)
        self.x_velocity = -1 * abs(math.cos(angle) * self.velocity)
        self.y_velocity = math.sin(angle) * self.velocity