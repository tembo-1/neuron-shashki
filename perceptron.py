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
            [0.0] * (self.in_sloy[1] + 64),
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
        betta = 2
        result = 0

        for g in range (len(gate)):
            self.new_gate[0][g] = gate[g]

        for i in range(self.num_sloy):
            for n in range(self.in_sloy[i]):
                work = 0
                for w in range( len(self.new_gate[i]) ):
                    if (i != self.num_sloy - 1):
                        work += self.sloy[i][n].weight[w] * self.new_gate[i][w]
                    else:
                        end_gate = self.new_gate[i][:10] + gate

                        work += self.sloy[i][n].weight[w] * end_gate[w]

                if (i != self.num_sloy - 1):
                    self.new_gate[i + 1][n] = 1 / (1 + math.exp( - betta * (work - self.sloy[i][n].porog) ))    
                else:
                    result = 1 / (1 + math.exp( - betta * (work - self.sloy[i][n].porog) ))

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

    def checkWhiteFood(self, desk, i, j, flag = False):
        left = copy.deepcopy(desk)
        right = copy.deepcopy(desk)
        result = []

        if (j < 6 and i < 6 and (left[i + 1][j + 1] == -1 or left[i + 1][j + 1] == -2) and left[i + 2][j + 2] == 0 and left[i][j] == 1):
            left[i][j] = 0
            left[i + 1][j + 1] = 0
            left[i + 2][j + 2] = 1

            if (i == 5):
                left[i + 2][j + 2] = 2
            
            nextLeftStep = self.checkWhiteFood(left, i + 2, j + 2, True)
            if (nextLeftStep):
                left = nextLeftStep

        if (j > 1 and i < 6 and (right[i + 1][j - 1] == -1 or right[i + 1][j - 1] == -2) and right[i + 2][j - 2] == 0 and right[i][j] == 1):
            right[i][j] = 0
            right[i + 1][j - 1] = 0
            right[i + 2][j - 2] = 1

            if (i == 5):
                right[i + 2][j - 2] = 2           
           
            nextRightStep = self.checkWhiteFood(right, i + 2, j - 2, True)
            if (nextRightStep):
                right = nextRightStep           

        if (right != desk and right):
            if (flag):
                result.extend(right)
            else:
                result.append(right)  
        if (left != desk and left):
            if (flag):
                result.extend(left)
            else:
                result.append(left)

        return result  

    def checkBlackFood(self, desk, i, j, flag = False):  
        left = copy.deepcopy(desk)
        right = copy.deepcopy(desk)
        result = []

        if (j < 6 and i > 1 and (right[i - 1][j + 1] == -1 or right[i - 1][j + 1] == -2) and right[i - 2][j + 2] == 0 and right[i][j] == 1):
            right[i][j] = 0
            right[i - 1][j + 1] = 0
            right[i - 2][j + 2] = 1

            if (i == 2):
                right[i - 2][j + 2] = 2             
                
            nextRightStep = self.checkBlackFood(right, i - 2, j + 2, True)
            if (nextRightStep):
                right = nextRightStep

        if (j > 1 and i > 1 and (left[i - 1][j - 1] == -1 or left[i - 1][j - 1] == -2) and left[i - 2][j - 2] == 0 and left[i][j] == 1):
            left[i][j] = 0
            left[i - 1][j - 1] = 0
            left[i - 2][j - 2] = 1 

            if (i == 2):
                left[i - 2][j - 2] = 2              
            
            nextLeftStep = self.checkBlackFood(left, i - 2, j - 2, True)
            if (nextLeftStep):
                left = nextLeftStep

        if (right != desk and right):
            if (flag):
                result.extend(right)
            else:
                result.append(right)  
        if (left != desk and left):
            if (flag):
                result.extend(left)
            else:
                result.append(left)

        return result   

    def checkBlackFoodQueen(self, desk, i, j, flag = False):
        top_left = copy.deepcopy(desk)
        top_right = copy.deepcopy(desk)
        bottom_left = copy.deepcopy(desk)
        bottom_right = copy.deepcopy(desk)
        result = []

        if (j < 6 and i > 1 and (top_left[i - 1][j + 1] == -1 or top_left[i - 1][j + 1] == -2) and top_left[i - 2][j + 2] == 0 and top_left[i][j] == 2):
            top_left[i][j] = 0
            top_left[i - 1][j + 1] = 0
            top_left[i - 2][j + 2] = 2           
                
            nextTopLeftStep = self.checkBlackFoodQueen(top_left, i - 2, j + 2, True)
            if (nextTopLeftStep):
                top_left = nextTopLeftStep

        if (j > 1 and i > 1 and (top_right[i - 1][j - 1] == -1 or top_right[i - 1][j - 1] == -2) and top_right[i - 2][j - 2] == 0 and top_right[i][j] == 2):
            top_right[i][j] = 0
            top_right[i - 1][j - 1] = 0
            top_right[i - 2][j - 2] = 2        

            nextTopRightStep = self.checkBlackFoodQueen(top_right, i - 2, j - 2, True)
            if (nextTopRightStep):
                top_right = nextTopRightStep            

        if (j < 6 and i < 6 and (bottom_left[i + 1][j + 1] == -1 or bottom_left[i + 1][j + 1] == -2) and bottom_left[i + 2][j + 2] == 0 and bottom_left[i][j] == 2):
            bottom_left[i][j] = 0
            bottom_left[i + 1][j + 1] = 0
            bottom_left[i + 2][j + 2] = 2
            
            nextBottomLeftStep = self.checkBlackFoodQueen(bottom_left, i + 2, j + 2, True)
            if (nextBottomLeftStep):
                bottom_left = nextBottomLeftStep

        if (j > 1 and i < 6 and (bottom_right[i + 1][j - 1] == -1 or bottom_right[i + 1][j - 1] == -2) and bottom_right[i + 2][j - 2] == 0 and bottom_right[i][j] == 2):
            bottom_right[i][j] = 0
            bottom_right[i + 1][j - 1] = 0
            bottom_right[i + 2][j - 2] = 2           
           
            nextBottomRightStep = self.checkBlackFoodQueen(bottom_right, i + 2, j - 2, True)
            if (nextBottomRightStep):
                bottom_right = nextBottomRightStep

        if (top_left != desk and top_left):
            if (flag):
                result.extend(top_left)
            else:
                result.append(top_left)  
        if (top_right != desk and top_right):
            if (flag):
                result.extend(top_right)
            else:
                result.append(top_right)
        if (bottom_left != desk and bottom_left):
            if (flag):
                result.extend(bottom_left)
            else:
                result.append(bottom_left)
        if (bottom_right != desk and bottom_right):
            if (flag):
                result.extend(bottom_right)
            else:
                result.append(bottom_right)                                

        return result 

    def checkWhiteFoodQueen(self, desk, i, j, flag = False):
        top_left = copy.deepcopy(desk)
        top_right = copy.deepcopy(desk)
        bottom_left = copy.deepcopy(desk)
        bottom_right = copy.deepcopy(desk)
        result = []

        if (j < 6 and i > 1 and (top_left[i - 1][j + 1] == -1 or top_left[i - 1][j + 1] == -2) and top_left[i - 2][j + 2] == 0 and top_left[i][j] == 2):
            top_left[i][j] = 0
            top_left[i - 1][j + 1] = 0
            top_left[i - 2][j + 2] = 2           
                
            nextTopLeftStep = self.checkWhiteFoodQueen(top_left, i - 2, j + 2, True)
            if (nextTopLeftStep):
                top_left = nextTopLeftStep

        if (j > 1 and i > 1 and (top_right[i - 1][j - 1] == -1 or top_right[i - 1][j - 1] == -2) and top_right[i - 2][j - 2] == 0 and top_right[i][j] == 2):
            top_right[i][j] = 0
            top_right[i - 1][j - 1] = 0
            top_right[i - 2][j - 2] = 2        

            nextTopRightStep = self.checkWhiteFoodQueen(top_right, i - 2, j - 2, True)
            if (nextTopRightStep):
                top_right = nextTopRightStep            

        if (j < 6 and i < 6 and (bottom_left[i + 1][j + 1] == -1 or bottom_left[i + 1][j + 1] == -2) and bottom_left[i + 2][j + 2] == 0 and bottom_left[i][j] == 2):
            bottom_left[i][j] = 0
            bottom_left[i + 1][j + 1] = 0
            bottom_left[i + 2][j + 2] = 2
            
            nextBottomLeftStep = self.checkWhiteFoodQueen(bottom_left, i + 2, j + 2, True)
            if (nextBottomLeftStep):
                bottom_left = nextBottomLeftStep

        if (j > 1 and i < 6 and (bottom_right[i + 1][j - 1] == -1 or bottom_right[i + 1][j - 1] == -2) and bottom_right[i + 2][j - 2] == 0 and bottom_right[i][j] == 2):
            bottom_right[i][j] = 0
            bottom_right[i + 1][j - 1] = 0
            bottom_right[i + 2][j - 2] = 2           
           
            nextBottomRightStep = self.checkWhiteFoodQueen(bottom_right, i + 2, j - 2, True)
            if (nextBottomRightStep):
                bottom_right = nextBottomRightStep

        if (top_left != desk and top_left):
            if (flag):
                result.extend(top_left)
            else:
                result.append(top_left)  
        if (top_right != desk and top_right):
            if (flag):
                result.extend(top_right)
            else:
                result.append(top_right)
        if (bottom_left != desk and bottom_left):
            if (flag):
                result.extend(bottom_left)
            else:
                result.append(bottom_left)
        if (bottom_right != desk and bottom_right):
            if (flag):
                result.extend(bottom_right)
            else:
                result.append(bottom_right)                                

        return result   

    def prepareDvumerium(self, desk):
        return [desk[i:i+8] for i in range(0, len(desk), 8)]

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

    def makePredicted(self, desk2, count, de = []):
        allGetExit = []
        maxStepsTwo = []
        maxStepsThree = []
        maxStepsFour = []
        maxStepsFive = []
        allGetExit3 = []
        maxGetExit2 = []
        maxGetExit3 = []
        maxGetExit1 = -10000
        number_i = 0
        step2 = []
        step3 = []
        step4 = []
        step5 = []


        for i in desk2:
            allGetExit.append(self.GetExit(i))

        for i in desk2:
            step = self.step(self.prepareDvumerium([-x for x in i]), count + 1)  
            if (not step):
                step2.append([[0] * 64])
            else:    
                step2.append(step)

        for i in step2:
            hren = []
            for j in i:
                if (all(element == 0 for element in j)):
                    hren.append(0)
                else:      
                    if (len(j) > 64):
                        pass                  
                    hren.append(self.GetExit(j))
            maxStepsTwo.append(i[hren.index(max(hren))])


        for i in maxStepsTwo:
            step = self.step(self.prepareDvumerium([-x for x in i]), count + 2)  
            if (not step):
                step3.append([[0] * 64])
            else:    
                step3.append(step)  
                    
        for i in step3:
            hren = []
            for j in i:
                if (all(element == 0 for element in j)):
                    hren.append(0)
                else:                        
                    if (len(j) > 64):
                        pass
                    hren.append(self.GetExit(j))
            maxStepsThree.append(i[hren.index(max(hren))])


            # for i in maxStepsThree:
            #     step = self.step(self.prepareDvumerium([-x for x in i]), count + 3)  
            #     if (not step):
            #         step4.append([[0] * 64])
            #     else:    
            #         step4.append(step)  


            # for i in step4:
            #     hren = []
            #     for j in i:
            #         if (all(element == 0 for element in j)):
            #             hren.append(0)
            #         else:                        
            #             hren.append(self.GetExit(j))
            #     maxStepsFour.append(i[hren.index(max(hren))])


            # for i in maxStepsFour:
            #     step = self.step(self.prepareDvumerium([-x for x in i]), count + 4)  
            #     if (not step):
            #         step5.append([[0] * 64])
            #     else:    
            #         step5.append(step)                      

            # for i in step5:
            #     hren = []
            #     for j in i:
            #         if (all(element == 0 for element in j)):
            #             hren.append(0)
            #         else:                        
            #             hren.append(self.GetExit(j))
            #     maxStepsFive.append(i[hren.index(max(hren))])
                           

        for i in maxStepsThree:
            allGetExit3.append(self.GetExit(i))
        
        return desk2[allGetExit3.index(max(allGetExit3))]

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
                            if (desk_temp1):
                                max_desk = []
                                for p in desk_temp1:                                
                                    max_desk.append(self.prepareData(p))

                                result_eat = []

                                for l in max_desk:
                                    if (len(l) > 64):
                                        split_arrays = [l[z:z+64] for z in range(0, len(l), 64)]
                                        result_eat.extend(split_arrays)
                                    else:
                                        result_eat.append(l)                                      
                                
                                return result_eat 

                            if (j < 7 and i < 7 and desk[i + 1][j + 1] == 0 and desk[i][j] == 1):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j + 1] = 1

                                if (i == 6):
                                    desk_temp[i + 1][j + 1] = 2 
                                
                                max_desk.append(self.prepareData(desk_temp))   
                                desk_temp = copy.deepcopy(desk)

                            if (j > 0 and i < 7 and desk[i + 1][j - 1] == 0 and desk[i][j] == 1):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j - 1] = 1

                                if (i == 6):
                                    desk_temp[i + 1][j - 1] = 2
                                  
                                max_desk.append(self.prepareData(desk_temp))  
                                desk_temp = copy.deepcopy(desk)   

                        except:
                            continue
                    elif (desk_temp[i][j] == 2):
                        try:
                            desk_temp1 = self.checkWhiteFoodQueen(desk_temp, i, j)
                            if (desk_temp1):
                                max_desk = []
                                for p in desk_temp1:                                
                                    max_desk.append(self.prepareData(p))

                                result_eat = [] 

                                for l in max_desk:
                                    if (len(l) > 64):
                                        split_arrays = [l[z:z+64] for z in range(0, len(l), 64)]
                                        result_eat.extend(split_arrays)
                                    else:
                                        result_eat.append(l)                                      
                                
                                return result_eat

                            if (j < 7 and i < 7 and desk[i + 1][j + 1] == 0 and desk[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j + 1] = 2 
                                max_desk.append(self.prepareData(desk_temp)) 
                                desk_temp = copy.deepcopy(desk)  

                            if (j > 0 and i < 7 and desk[i + 1][j - 1] == 0 and desk[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j - 1] = 2
                                max_desk.append(self.prepareData(desk_temp)) 
                                desk_temp = copy.deepcopy(desk)  

                            if (j < 7 and i > 0 and desk[i - 1][j + 1] == 0 and desk[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j + 1] = 2
                                max_desk.append(self.prepareData(desk_temp))
                                desk_temp = copy.deepcopy(desk)  

                            if (j > 0 and i > 0 and desk[i - 1][j - 1] == 0 and desk[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j - 1] = 2                                 
                                max_desk.append(self.prepareData(desk_temp))
                                desk_temp = copy.deepcopy(desk)  

                        except:
                            continue                             
                else:        
                    if (desk_temp[i][j] == 1):
                        try:
                            desk_temp1 = self.checkBlackFood(desk_temp, i, j)
                            if (desk_temp1):
                                max_desk = []
                                for p in desk_temp1:                                
                                    max_desk.append(self.prepareData(p))

                                result_eat = [] 

                                for l in max_desk:
                                    if (len(l) > 64):
                                        split_arrays = [l[z:z+64] for z in range(0, len(l), 64)]
                                        result_eat.extend(split_arrays)
                                    else:
                                        result_eat.append(l)                                      
                                
                                return result_eat 

                            if (j < 7 and i > 0 and desk[i - 1][j + 1] == 0 and desk[i][j] == 1):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j + 1] = 1

                                if (i == 1):
                                    desk_temp[i - 1][j + 1] = 2
                                max_desk.append(self.prepareData(desk_temp))
                                desk_temp = copy.deepcopy(desk)  

                            if (j > 0 and i > 0 and desk[i - 1][j - 1] == 0 and desk[i][j] == 1):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j - 1] = 1

                                if (i == 1):
                                    desk_temp[i - 1][j - 1] = 2
                                max_desk.append(self.prepareData(desk_temp))
                                desk_temp = copy.deepcopy(desk)  

                        except:
                            continue

                    elif (desk_temp[i][j] == 2):
                        try:
                            desk_temp1 = self.checkBlackFoodQueen(desk_temp, i, j)
                            if (desk_temp1):
                                max_desk = []
                                for p in desk_temp1:                                
                                    max_desk.append(self.prepareData(p))

                                result_eat = [] 

                                for l in max_desk:
                                    if (len(l) > 64):
                                        split_arrays = [l[z:z+64] for z in range(0, len(l), 64)]
                                        result_eat.extend(split_arrays)
                                    else:
                                        result_eat.append(l)                                      
                                
                                return result_eat

                            if (j < 7 and i < 7 and desk[i + 1][j + 1] == 0 and desk[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j + 1] = 2  
                                max_desk.append(self.prepareData(desk_temp))                              
                                desk_temp = copy.deepcopy(desk)  

                            if (j > 0 and i < 7 and desk[i + 1][j - 1] == 0 and desk[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i + 1][j - 1] = 2
                                max_desk.append(self.prepareData(desk_temp))       
                                desk_temp = copy.deepcopy(desk)                          

                            if (j < 7 and i > 0 and desk[i - 1][j + 1] == 0 and desk[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j + 1] = 2
                                max_desk.append(self.prepareData(desk_temp))     
                                desk_temp = copy.deepcopy(desk)                            

                            if (j > 0 and i > 0 and desk[i - 1][j - 1] == 0 and desk[i][j] == 2):
                                desk_temp[i][j] = 0
                                desk_temp[i - 1][j - 1] = 2
                                max_desk.append(self.prepareData(desk_temp))  
                                desk_temp = copy.deepcopy(desk)                                
                                  
                        except:
                            continue                         


        return max_desk        
                       