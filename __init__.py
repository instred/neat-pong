from game import Game
import pygame

width = 1200
height = 700

class Pong:
    
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball  


    def test(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.left_paddle.move(up=True)
            if keys[pygame.K_s]:
                self.game.left_paddle.move(up=False)



            self.game.draw(True, False)
            pygame.display.update()

window = pygame.display.set_mode((width,height))
p = Pong(window, width, height)
p.test()