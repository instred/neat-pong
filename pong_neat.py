import pygame
from game import Game, GameInfo
import neat
import os
import pickle

class Pong:
    
    def __init__(self, window, width, height) -> None:
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball  

    def test(self, genome, config) -> None:
        network = neat.nn.FeedForwardNetwork.create(genome, config)

        #standard game loop

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
                self.game.movePaddle()
            if keys[pygame.K_s]:
                self.game.movePaddle(up=False)

            out = network.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            dec = out.index(max(out))

            match(dec):
                case 0:
                    pass
                case 1:
                    self.game.movePaddle(left=False, up=True)
                case _:
                    self.game.movePaddle(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw(True, True)
            pygame.display.update()



    #function for training the ai with itself

    def train(self, genome, genome2, config) -> None:
        network1 = neat.nn.FeedForwardNetwork.create(genome, config)
        network2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            
            # using 3 input values for the network - paddle y cord, ball y cord and distance between ball and paddle    
            out1 = network1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            dec1 = out1.index(max(out1))

            match(dec1):
                case 0:
                    pass
                case 1:
                    self.game.movePaddle(left=True, up=True)
                case _:
                    self.game.movePaddle(left=True, up=False)

            out2 = network2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            dec2 = out2.index(max(out2))

            match(dec2):
                case 0:
                    pass
                case 1:
                    self.game.movePaddle(left=False, up=True)
                case _:
                    self.game.movePaddle(left=False, up=False)
            

            info = self.game.loop()
            
            self.game.draw(draw_score=True, draw_hits=True)
            pygame.display.update()

            if info.left_score >= 1 or info.right_score >= 1 or info.left_hits > 50:
                self.calculate_fitness(genome, genome2, info)
                break

    # fitness value of each genome

    def calculate_fitness(self, genome, genome2, info : GameInfo) -> None:
        genome.fitness += info.left_hits
        genome2.fitness += info.right_hits


# setting up the fitnesses of my genomes

def eval_genomes(genomes, config) -> None:
    window_width, window_height = 1200, 700
    window = pygame.display.set_mode((window_width, window_height))
    
    for i, (gen_id, genome) in enumerate(genomes):
        if i == len(genomes) - 1:
            break

        genome.fitness = 0
        for (gen2_id, genome2) in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            game = Pong(window, window_width, window_height)
            game.train(genome, genome2, config)

def run(config) -> None:
    # to restore from a checkpoint

    pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-9')
    
    # new population
    #pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))

    #save best one as pickle
    winner_ai = pop.run(eval_genomes, 15)
    with open("best.pickle", "wb") as winner_file:
        pickle.dump(winner_ai, winner_file)


# load best ai saved as pickle
def load_ai(config) -> None:
    with open("best.pickle", "rb") as winner_file:
        winner = pickle.load(winner_file)

    window_width, window_height = 1200, 700
    window = pygame.display.set_mode((window_width, window_height))

    game = Pong(window, window_width, window_height)
    game.test(winner, config)


if __name__ == '__main__':
    local = os.path.dirname(__file__)
    config_path = os.path.join(local, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # training ai
    # run(config)

    # playing vs ai
    load_ai(config)