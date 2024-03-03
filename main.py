import pygame
from pong import Game
import neat
import os
import pickle

def run_neat(config):
    pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-6')
    # pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    pop.add_reporter(neat.Checkpointer(2))

    winner = pop.run(eval_genomes, 1)

    with open("best.pickle", "wb") as file:
        pickle.dump(winner, file)

def against_ai(config):
    width, height = 700, 500
    wind = pygame.display.set_mode((width, height))

    with open("violett.pickle", "rb") as file:
        ai = pickle.load(file)

    game = PongGame(wind, width, height)
    game.test_ai(ai, config)

def eval_genomes(genomes, config):
    width, height = 700, 500
    wind = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        # This i+1 will prevent from game to repeat
        # So the genome 25 will play genomes from 26 to end
        for genome_id2, genome2 in genomes[i+1:]:
            # It verifies if the genome already has the fitness attribute
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(wind, width, height)
            game.train_ai(genome1, genome2, config)

class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            elif keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            #if keys[pygame.K_UP]:
            #    game.move_paddle(left=False, up=True)
            #elif keys[pygame.K_DOWN]:
            #    game.move_paddle(left=False, up=False)

            outputs = net.activate((self.ball.y, self.right_paddle.y, abs(self.right_paddle.x - self.ball.x)))

            if outputs.index(max(outputs)) == 1:
                self.game.move_paddle(left=False, up=True)
            elif outputs.index(max(outputs)) == 0:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw()
            pygame.display.update()

            if game_info.left_score >= 10 or game_info.right_score >= 10: 
                break

        pygame.quit()

    def train_ai(self, genome1, genome2, config):
        run = True
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config) 
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            
            outputs1 = net1.activate((self.ball.y, self.left_paddle.y, abs(self.left_paddle.x - self.ball.x)))
            outputs2 = net2.activate((self.ball.y, self.right_paddle.y, abs(self.right_paddle.x - self.ball.x)))

            if outputs1.index(max(outputs1)) == 1:
                self.game.move_paddle(left=True, up=True)
            elif outputs1.index(max(outputs1)) == 0:
                self.game.move_paddle(left=True, up=False)

            if outputs2.index(max(outputs2)) == 1:
                self.game.move_paddle(left=False, up=True)
            elif outputs2.index(max(outputs2)) == 0:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()

            self.game.draw(True, True)
            pygame.display.update()

            if game_info.left_score >= 2 or game_info.right_score >= 2 or game_info.left_hits > 50:
                self.calculate_fitness(genome1, genome2, game_info)
                break

    def calculate_fitness(self, genome1, genome2, game_info):
        genome1.fitness += game_info.left_hits + game_info.left_score
        genome2.fitness += game_info.right_hits + game_info.right_score


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    #run_neat(config)
    against_ai(config)
