import random

class Neuron:

    def __init__(self,
                 size: int,
                 ):
        self.porog = random.uniform(-0.5, 0.5)
        self.weight = []

        for i in range(size):
            self.weight.append( random.uniform(-0.5, 0.5) )        
