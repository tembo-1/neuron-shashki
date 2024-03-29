from perceptron import Perceptron
from population import *
from game import *
import json

education = int(input('Обучать - 1, не обучать - 0: '))

if (education):
    population = Population ()

    evolution = 100

    for i in range(evolution):
        print(i)
        count = population.Selection()
        population.Reproduction()
        population.Mutate()
        if i % 5 == 0:
            data = population.person

            winner:Perceptron
            max = -1000

            for w in data:
                if (w.score >= max):
                    winner = w

            data = []

            for k in range(3):
                for j in range(winner.in_sloy[k]):
                    data.append({"neuron" : j, "sloy": k, "porog" : winner.sloy[k][j].porog, "weight" : winner.sloy[k][j].weight})

            with open('data.json', 'w') as f:
                json.dump(data, f)  


    data = population.person

    winner:Perceptron
    max = -1000

    for i in data:
        if (i.score > max):
            winner = i

    data = []

    for i in range(3):
        for j in range(winner.in_sloy[i]):
            data.append({"neuron" : j, "sloy": i, "porog" : winner.sloy[i][j].porog, "weight" : winner.sloy[i][j].weight})
        
    with open('data.json', 'w') as f:
        json.dump(data, f)


type = int(input("Type game: "))
game = Game(type)

if (type == 1):
    game.StepOwn(int(input("Your step in cell: ")))


while(not game.victory):
    game.StepEnemy()
    game.StepOwn(int(input("Your step in cell: ")))        

