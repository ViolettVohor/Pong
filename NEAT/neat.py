import neat
import os
from PONG.solution import PongGame

def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = p.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)

def eval_genomes(genomes, config):
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness == 0 if genome2.fitness == None else genome2.fitness
            game = PongGame()
            train_ai(game, [genome1, genome2], config)

def train_ai(game, genomes, config):
    net1 = neat.nn.feedfowardnetwork.create(genome1, config) 
    net2 = neat.nn.feedfowardnetwork.create(genome2, config) 

def move_ai(net, ball, paddle):
    output = net.activate((ball.y, paddle.y, abs(ball.x - paddle.x))) 
    print(output)

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config.txt")

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                config_path)

run_neat(config)
