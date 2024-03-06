from PONG.solution import *
from PONG.const import *
import neat

def start_ai(genomes, config):
    nets = [None, None]
    if genomes[0] != None:
        nets[0] = neat.nn.FeedForwardNetwork.create(genomes[0], config)
    if genomes[1] != None:
        nets[1] = neat.nn.FeedForwardNetwork.create(genomes[1], config)

    return nets

def loop_ai(nets, info, config):
    for i in range(0, len(nets)):
        if nets[i] != None:
            outputs = nets[i].activate((info[0].y, info[i+1].y, abs(info[i+1].x - info[0].x)))

            if (outputs.index(max(outputs)) == 1 and 
                info[i+1].y - VEL > 0):
                info[i+1].move(up=True)
            elif (outputs.index(max(outputs)) == 2 and 
                  info[i+1].y + VEL < HEIGHT - PADDLE_HEIGHT):
                info[i+1].move(up=False)
