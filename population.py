from perceptron import *
import random as rnd

class Population:
    def __init__(self):
        self.size = 10
        self.half_size = int(self.size/2)
        self.mutate = 0.02
        self.person = []
        self.num_sloy = 3
        self.count = 1
        self.victory_combined = [
		    [0, 4, 8],
		    [2, 4, 6],
		    [0, 1, 2],
		    [3, 4, 5],
		    [6, 7, 8],
		    [0, 3, 6],
		    [1, 4, 7],
		    [2, 5, 8],
        ]

        for i in range(self.size):
            self.person.append( Perceptron() )

    def checkWin(self, desk):
        minus_one_found = True
        one_found = True
        for row in desk:
            for elem in row:
                if elem == -1 or elem == -2:
                    minus_one_found = False
                if elem == 1 or elem == 2:
                    one_found = False

        return minus_one_found ^ one_found


    def Game(self, white : Perceptron, black : Perceptron):
        desk = [[0 for j in range(8)] for i in range(8)]

        for i in range(3):
            for j in range(8):
                if (i % 2 and not j % 2):
                    desk[i][j] = 1
                elif (not i % 2 and j % 2):
                    desk[i][j] = 1 

        for i in range(3):
            for j in range(8):
                if (not i % 2 and not j % 2):
                    desk[7-i][j] = -1
                elif ( i % 2 and  j % 2):
                    desk[7-i][j] = -1 


        victory = False

        while not victory:
            try:   
                if (self.count > 200):                  
                    break           

                step = white.step(desk, self.count)

                if (self.checkWin(step)):
                    white.score += 1
                    black.score -= 2
                    break

                desk = white.makePredicted(step, self.count)
                desk = white.prepareDvumerium(desk)

                self.count += 1

                step = black.step(desk, self.count)

                if (self.checkWin(step)):
                    white.score += 1
                    black.score -= 2
                    break

                desk = black.makePredicted(step, self.count)
                desk = black.prepareDvumerium(desk)

                self.count += 1
            except:
                break
   
    def Selection(self):
        temp_person = []

        for i in self.person:
            i.score = 0.0

        for i in range(self.size):
            for j in range(5):
                rand = int(random.uniform(0, self.size))
                while (i == rand):
                    rand = int(random.uniform(0, self.size))
                self.Game(self.person[i], self.person[j])

        for i in self.person:
            temp_person.append(i)
     
        score_person = 0.0
        for i in self.person:
            score_person += i.score

        print("Общий счёт", score_person)

        self.person = sorted(temp_person, key=lambda Perceptron: Perceptron.score, reverse=True)[:-self.half_size]

        return score_person

    def Reproduction(self):
        for i in range(self.half_size):
            parent1 = int(random.uniform(0, self.half_size))
            parent2 = int(random.uniform(0, self.half_size))

            while parent1 == parent2:
                parent2 = int(random.uniform(0, self.half_size))    

            self.person.append( self.person[parent1].Crossover(self.person[parent2]) )  

    def Mutate(self):
        for i in self.person:
            i.Mutating(self.mutate)
        