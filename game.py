import pygame
from paddle import Paddle
from ball import Ball

pygame.init()

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class GameInfo:
    def __init__(self, left_hits, right_hits, left_score, right_score) -> None:
        self.left_score = left_score
        self.right_score = right_score
        self.left_hits = left_hits
        self.right_hits = right_hits

class Game:

    def __init__(self, window, window_width, window_height) -> None:
        self.window = window
        self.window_height = window_height
        self.window_width = window_width

        # paddle initializing

        self.left_paddle = Paddle(5, self.window_height // 2 - Paddle.height // 2)

        self.right_paddle = Paddle(self.window_width - 5 - Paddle.width, self.window_height // 2 - Paddle.height // 2)

        # ball init

        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        self.left_score : int = 0
        self.right_score : int = 0
        self.left_hits : int = 0
        self.right_hits : int = 0
    
    def drawScore(self) -> None:
        left_score_text = SCORE_FONT.render(f"{self.left_score}", 1, WHITE)
        right_score_text = SCORE_FONT.render(f"{self.right_score}", 1, WHITE)

        self.window.blit(left_score_text, (self.window_width //
                                4 - left_score_text.get_width()//2, 20))
        self.window.blit(right_score_text, (self.window_width * (3/4) -
                                right_score_text.get_width()//2, 20))

    def drawHits(self) -> None:
        hits_text = SCORE_FONT.render(f"{self.left_hits + self.right_hits}", 1, RED)
        
        self.window.blit(hits_text, (self.window_width // 2 - hits_text.get_width()//2, 10))

    def drawLine(self) -> None:
        pygame.draw.rect(self.window, WHITE, (self.window_width //2, 2, 3, self.window_height))

    def draw(self, draw_score=True, draw_hits=False) -> None:
        self.window.fill(BLACK)

        self.drawLine()

        if draw_score:
            self.drawScore()

        if draw_hits:
            self.drawHits()

        #paddle draw

        self.left_paddle.draw(self.window)
        self.right_paddle.draw(self.window)

        #ball draw

        self.ball.draw(self.window)

    def movePaddle(self, left=True, up=True) -> bool:

        # returns false if paddle would go offscreen
        if left:

            if up and self.left_paddle.y - Paddle.velocity < 0:
                return False
            if not up and self.left_paddle.y + Paddle.height > self.window_height:
                return False
            self.left_paddle.move(up)
        else:

            if up and self.right_paddle.y - Paddle.velocity < 0:
                return False
            if not up and self.right_paddle.y + Paddle.height > self.window_height:
                return False
            self.right_paddle.move(up)

        return True
    
    def collisions(self) -> None:
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        if ball.y + ball.radius >= self.window_height:
            ball.y_velocity *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_velocity *= -1

        if ball.x_velocity < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.height:
                if ball.x - ball.radius <= left_paddle.x + Paddle.width:
                    ball.x_velocity *= -1

                    middle_y = left_paddle.y + Paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.height / 2) / ball.velocity
                    y_vel = difference_in_y / reduction_factor
                    ball.y_velocity = -1 * y_vel
                    self.left_hits += 1

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + Paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_velocity *= -1

                    middle_y = right_paddle.y + Paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.height / 2) / ball.velocity
                    y_vel = difference_in_y / reduction_factor
                    ball.y_velocity = -1 * y_vel
                    self.right_hits += 1


    def loop(self) -> GameInfo:

        game_info = GameInfo(
            self.left_hits, self.right_hits, self.left_score, self.right_score)
        
        # ball moving + collision

        self.ball.move()
        self.collisions()

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.left_score += 1

        return game_info
    
    def reset(self) -> None:
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0

        # objects resets

        self.left_paddle.reset()
        self.right_paddle.reset()
