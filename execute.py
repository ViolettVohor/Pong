from PONG.solution import game
import pickle
import neat

def run_neat(config):
    pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-20')
    #pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    pop.add_reporter(neat.Checkpointer(1))

    best = pop.run(eval_genomes, 1)

    with open("best.pickle", "wb") as file:
        pickle.dump(best, file)

def eval_genomes(genomes, config):
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            main([genome1, genome2], config, True, False)
