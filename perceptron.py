import random
import math
from neuron import Neuron
import copy
import json

class Perceptron:

    def __init__(self):
        self.num_gate = 64
        self.in_sloy = [40, 10, 1]
        self.inputNeuron = [64, 40, 10, 1]
        self.num_sloy = 3
        self.score = 0
        self.new_gate = [
            [0.0] * self.num_gate,
            [0.0] * self.in_sloy[0],
            [0.0] * self.in_sloy[1],
            [0.0] * self.in_sloy[2],
        ]
        self.sloy = []

        for i in range( len(self.in_sloy) ):
            my_neyron = []
            for j in range(self.in_sloy[i]):
                my_neyron.append(  Neuron(len(self.new_gate[i])) )
            self.sloy.append(my_neyron)

    def read(self):
        with open('data.json') as file:
            data = json.load(file)

        for i in range(self.num_sloy):
            for j in range(self.in_sloy[i]):
                for n in data:
                    if (n['neuron'] == j and n['sloy'] == i):
                        self.sloy[i][j].porog = n['porog']
                        self.sloy[i][j].weight = n['weight']              

    def GetExit(self, gate):
        betta = 1
        result = 0

        for g in range (len(gate)):
            self.new_gate[0][g] = gate[g]


        for i in range(self.num_sloy):
            for n in range(self.in_sloy[i]):
                work = 0
                for w in range( len(self.new_gate[i]) ):
                    work += self.sloy[i][n].weight[w] * self.new_gate[i][w]
                if (i != self.num_sloy - 1):
                    self.new_gate[i + 1][n] = 1 / (1 + math.exp( -betta * (work - self.sloy[i][n].porog) ))    
                else:
                    result = 1 / (1 + math.exp( -betta * (work - self.sloy[i][n].porog) ))

        return result

    def Crossover(self, parent):
        same = random.uniform(0, 1)
        child = Perceptron()

        for i in range(self.num_sloy):
            for j in range(self.in_sloy[i]):
                child.sloy[i][j].porog = same * self.sloy[i][j].porog + (1 - same) * parent.sloy[i][j].porog
                for k in range(len(self.new_gate[i])):
                    child.sloy[i][j].weight[k] = same * self.sloy[i][j].weight[k] + (1 - same) * parent.sloy[i][j].weight[k]

        return child                
        
    def Mutating(self, mutate):
        for i in range(self.num_sloy):
            for j in range(self.in_sloy[i]):
                self.sloy[i][j].porog *= random.uniform(1 - mutate, 1 + mutate)
                for k in range(len(self.new_gate[i])):
                    self.sloy[i][j].weight[k] *= random.uniform(1 - mutate, 1 + mutate)

    def prepareData(self, data):
        desk = []
        for i in data:
            for j in i:
                desk.append(j)
        return desk

    def checkWhiteFood(self, desk, i, j):
        desk1 = copy.deepcopy(desk)
        if (j < 6 and i < 6 and (desk1[i + 1][j + 1] == -1 or desk1[i + 1][j + 1] == -2) and desk1[i + 2][j + 2] == 0 and desk1[i][j] == 1):
            desk1[i][j] = 0
            desk1[i + 1][j + 1] = 0
            desk1[i + 2][j + 2] = 1

            if (i == 5):
                desk1[i + 2][j + 2] = 2
            
            desk1 = self.checkWhiteFood(desk1, i + 2, j + 2)

        if (j > 1 and i < 6 and (desk1[i + 1][j - 1] == -1 or desk1[i + 1][j - 1] == -2) and desk1[i + 2][j - 2] == 0 and desk1[i][j] == 1):
            desk1[i][j] = 0
            desk1[i + 1][j - 1] = 0
            desk1[i + 2][j - 2] = 1

            if (i == 5):
                desk1[i + 2][j - 2] = 2           
           
            desk1 = self.checkWhiteFood(desk1, i + 2, j - 2)

        return desk1  

    def checkBlackFood(self, desk, i, j):  
        desk1 = copy.deepcopy(desk)

        if (j < 6 and i > 1 and (desk1[i - 1][j + 1] == 1 or desk1[i - 1][j + 1] == 2) and desk1[i - 2][j + 2] == 0 and desk1[i][j] == -1):
            desk1[i][j] = 0
            desk1[i - 1][j + 1] = 0
            desk1[i - 2][j + 2] = -1

            if (i == 2):
                desk1[i - 2][j + 2] = -2             
                
            desk1 = self.checkBlackFood(desk1, i - 2, j + 2)

        if (j > 1 and i > 1 and (desk1[i - 1][j - 1] == 1 or desk1[i - 1][j - 1] == 2) and desk1[i - 2][j - 2] == 0 and desk1[i][j] == -1):
            desk1[i][j] = 0
            desk1[i - 1][j - 1] = 0
            desk1[i - 2][j - 2] = -1 

            if (i == 2):
                desk1[i - 2][j - 2] = -2              
            
            desk1 = self.checkBlackFood(desk1, i - 2, j - 2)

        return desk1   

    def checkBlackFoodQueen(self, desk, i, j):
        desk1 = copy.deepcopy(desk)

        if (j < 6 and i > 1 and (desk1[i - 1][j + 1] == 1 or desk1[i - 1][j + 1] == 2) and desk1[i - 2][j + 2] == 0 and desk1[i][j] == -2):
            desk1[i][j] = 0
            desk1[i - 1][j + 1] = 0
            desk1[i - 2][j + 2] = -2            
                
            desk1 = self.checkBlackFoodQueen(desk1, i - 2, j + 2)

        if (j > 1 and i > 1 and (desk1[i - 1][j - 1] == 1 or desk1[i - 1][j - 1] == 2) and desk1[i - 2][j - 2] == 0 and desk1[i][j] == -2):
            desk1[i][j] = 0
            desk1[i - 1][j - 1] = 0
            desk1[i - 2][j - 2] = -2              
            
            desk1 = self.checkBlackFoodQueen(desk1, i - 2, j - 2)

        if (j < 6 and i < 6 and (desk1[i + 1][j + 1] == 1 or desk1[i + 1][j + 1] == 2) and desk1[i + 2][j + 2] == 0 and desk1[i][j] == -2):
            desk1[i][j] = 0
            desk1[i + 1][j + 1] = 0
            desk1[i + 2][j + 2] = -2
            
            desk1 = self.checkBlackFoodQueen(desk1, i + 2, j + 2)

        if (j > 1 and i < 6 and (desk1[i + 1][j - 1] == 1 or desk1[i + 1][j - 1] == 2) and desk1[i + 2][j - 2] == 0 and desk1[i][j] == -2):
            desk1[i][j] = 0
            desk1[i + 1][j - 1] = 0
            desk1[i + 2][j - 2] = -2         
           
            desk1 = self.checkBlackFoodQueen(desk1, i + 2, j - 2)

        return desk1 

    def checkWhiteFoodQueen(self, desk, i, j):
        desk1 = copy.deepcopy(desk)

        if (j < 6 and i > 1 and (desk1[i - 1][j + 1] == -1 or desk1[i - 1][j + 1] == -2) and desk1[i - 2][j + 2] == 0 and desk1[i][j] == 2):
            desk1[i][j] = 0
            desk1[i - 1][j + 1] = 0
            desk1[i - 2][j + 2] = 2           
                
            desk1 = self.checkWhiteFoodQueen(desk1, i - 2, j + 2)

        if (j > 1 and i > 1 and (desk1[i - 1][j - 1] == -1 or desk1[i - 1][j - 1] == -2) and desk1[i - 2][j - 2] == 0 and desk1[i][j] == 2):
            desk1[i][j] = 0
            desk1[i - 1][j - 1] = 0
            desk1[i - 2][j - 2] = 2            
            
            desk1 = self.checkWhiteFoodQueen(desk1, i - 2, j - 2)

        if (j < 6 and i < 6 and (desk1[i + 1][j + 1] == -1 or desk1[i + 1][j + 1] == -2) and desk1[i + 2][j + 2] == 0 and desk1[i][j] == 2):
            desk1[i][j] = 0
            desk1[i + 1][j + 1] = 0
            desk1[i + 2][j + 2] = 2
            
            desk1 = self.checkWhiteFoodQueen(desk1, i + 2, j + 2)

        if (j > 1 and i < 6 and (desk1[i + 1][j - 1] == -1 or desk1[i + 1][j - 1] == -2) and desk1[i + 2][j - 2] == 0 and desk1[i][j] == 2):
            desk1[i][j] = 0
            desk1[i + 1][j - 1] = 0
            desk1[i + 2][j - 2] = 2           
           
            desk1 = self.checkWhiteFoodQueen(desk1, i + 2, j - 2)

        return desk1   

    def prepareDvumerium(self, desk):
        return [desk[i:i+8] for i in range(0, len(desk), 8)]

    def makePredicted(self, desk2, count):
        allGetExit = []
        allGetExit2 = []
        maxGetExit2 = []
        maxGetExit1 = 0
        number_i = 0
        step2 = []

        for i in desk2:
            allGetExit.append(self.GetExit(i))
            
        for i in desk2:
            step2.append(self.step(self.prepareDvumerium(i), count + 1))
            print(len(step2))

        for i in step2:
            hren = []
            for j in i:
                hren.append(self.GetExit(j))
            allGetExit2.append(hren)

        for k in allGetExit2:
            if (len(k) == 0):
                print('-------------------------')
                for j in step2:
                    print(self.prepareData(j))

            maxGetExit2.append(max(k))

        for i in range(len(allGetExit)):
            if (allGetExit[i] - maxGetExit2[i] > maxGetExit1):
                maxGetExit1 = allGetExit[i] - maxGetExit2[i]
                number_i = i

        return desk2[number_i]


    def step(self, desk, count):
        max = -100
        max_desk = []
        for i in range(len(desk)):
            for j in range(len(desk)):

                desk_temp = copy.deepcopy(desk)

                if (count % 2):
                    if (desk_temp[i][j] == 1):
                        try:
                            desk_temp1 = self.checkWhiteFood(desk_temp, i, j)
                            if (desk_temp1 != desk_temp):
                                max_desk = []
                                max_desk.append(self.prepareData(desk_temp1))
                                return max_desk

                            if (j < 7 and i < 7 and desk_temp[i + 1][j + 1] == 0 and desk_temp[i][j] == 1):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j + 1] = 1

                                if (i == 6):
                                    desk_temp[i + 1][j + 1] = 2 
                                max_desk.append(self.prepareData(desk_temp))    

                            if (j > 0 and i < 7 and desk_temp[i + 1][j - 1] == 0 and desk_temp[i][j] == 1):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j - 1] = 1

                                if (i == 6):
                                    desk_temp[i + 1][j - 1] = 2
                                max_desk.append(self.prepareData(desk_temp))     

                        except:
                            continue
                    elif (desk_temp[i][j] == 2):
                        try:
                            desk_temp1 = self.checkWhiteFoodQueen(desk_temp, i, j)

                            if (desk_temp1 != desk_temp):
                                max_desk = []
                                max_desk.append(self.prepareData(desk_temp1))
                                return max_desk

                            if (j < 7 and i < 7 and desk_temp[i + 1][j + 1] == 0 and desk_temp[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j + 1] = 2 
                                max_desk.append(self.prepareData(desk_temp)) 

                            if (j > 0 and i < 7 and desk_temp[i + 1][j - 1] == 0 and desk_temp[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j - 1] = 2
                                max_desk.append(self.prepareData(desk_temp)) 

                            if (j < 7 and i > 0 and desk_temp[i - 1][j + 1] == 0 and desk_temp[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j + 1] = 2
                                max_desk.append(self.prepareData(desk_temp))

                            if (j > 0 and i > 0 and desk_temp[i - 1][j - 1] == 0 and desk_temp[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j - 1] = 2                                 
                                max_desk.append(self.prepareData(desk_temp))

                        except:
                            continue 

                                                
                else:        
                    if (desk_temp[i][j] == -1):
                        try:
                            desk_temp1 = self.checkBlackFood(desk_temp, i, j)

                            if (desk_temp1 != desk_temp):
                                max_desk = []
                                max_desk.append(self.prepareData(desk_temp1))
                                return max_desk

                            if (j < 7 and i > 0 and desk_temp[i - 1][j + 1] == 0 and desk_temp[i][j] == -1):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j + 1] = -1

                                if (i == 1):
                                    desk_temp[i - 1][j + 1] = -2
                                max_desk.append(self.prepareData(desk_temp))

                            if (j > 0 and i > 0 and desk_temp[i - 1][j - 1] == 0 and desk_temp[i][j] == -1):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j - 1] = -1

                                if (i == 1):
                                    desk_temp[i - 1][j - 1] = -2
                                max_desk.append(self.prepareData(desk_temp))

                        except:
                            continue

                    elif (desk_temp[i][j] == -2):
                        try:
                            desk_temp1 = self.checkBlackFoodQueen(desk_temp, i, j)

                            if (desk_temp1 != desk_temp):
                                max_desk = []
                                max_desk.append(self.prepareData(desk_temp1))
                                return max_desk

                            if (j < 7 and i < 7 and desk_temp[i + 1][j + 1] == 0 and desk_temp[i][j] == -2):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j + 1] = -2  
                                max_desk.append(self.prepareData(desk_temp))                              

                            if (j > 0 and i < 7 and desk_temp[i + 1][j - 1] == 0 and desk_temp[i][j] == -2):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j - 1] = -2
                                max_desk.append(self.prepareData(desk_temp))                               

                            if (j < 7 and i > 0 and desk_temp[i - 1][j + 1] == 0 and desk_temp[i][j] == -2):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j + 1] = -2
                                max_desk.append(self.prepareData(desk_temp))                               

                            if (j > 0 and i > 0 and desk_temp[i - 1][j - 1] == 0 and desk_temp[i][j] == -2):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j - 1] = -2
                                max_desk.append(self.prepareData(desk_temp))                                
                                  

                        except:
                            continue                         

        if max_desk == [[]]:
            pass
        return max_desk        
                       