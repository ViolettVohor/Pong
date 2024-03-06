import neat
import os
from execute import *

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config.txt")

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

run_neat(config)
#against_ai(config)
#main()
