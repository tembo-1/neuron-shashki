from perceptron import *
import os

class Game:
    def __init__(self, type : int):
        self.enemy = Perceptron()
        self.enemy.read()
        self.desk = [[0 for j in range(8)] for i in range(8)]
        self.count = 1

        for i in range(3):
            for j in range(8):
                if (i % 2 and not j % 2):
                    self.desk[i][j] = 1
                elif (not i % 2 and j % 2):
                    self.desk[i][j] = 1 

        for i in range(3):
            for j in range(8):
                if (not i % 2 and not j % 2):
                    self.desk[7-i][j] = -1
                elif ( i % 2 and  j % 2):
                    self.desk[7-i][j] = -1 


        self.number = 1
        self.type = type
        self.victory = False
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
        
        if (len(desk2[0]) == 0):
            pass

        for i in desk2:
            allGetExit.append(self.GetExit(i))
            
        for i in desk2:
            step2.append(self.step(self.prepareDvumerium(i), count + 1))

        for i in step2:
            hren = []
            for j in i:
                hren.append(self.GetExit(j))
            allGetExit2.append(hren)

        for k in allGetExit2:
            if (len(k) == 0):
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

    def prepareDvumerium(self, desk):
        return [desk[i:i+8] for i in range(0, len(desk), 8)]

    def StepEnemy(self):
        self.desk = self.prepareDvumerium(self.enemy.makePredicted(self.desk, self.count))

    def StepOwn(self, desk_temp, x1, y1, x2, y2):
        if (self.checkWin(desk_temp)):
            return True
        for i in range(8):
            for j in range(8):
                if (self.count % 2):
                    if (desk_temp[i][j] == 1):
                        try:
                            desk_temp1 = self.checkWhiteFood(desk_temp, i, j)
                            if (desk_temp1 != desk_temp):
                                return desk_temp1   
                        except:
                            continue
                    elif (desk_temp[i][j] == 2):
                        try:
                            desk_temp1 = self.checkWhiteFoodQueen(desk_temp, i, j)
                            if (desk_temp1 != desk_temp):
                                return desk_temp1
                        except:
                            continue                    
                else:        
                    if (desk_temp[i][j] == -1):
                        try:
                            desk_temp1 = self.checkBlackFood(desk_temp, i, j)
                            if (desk_temp1 != desk_temp):
                                return desk_temp1
                        except:
                            continue

                    elif (desk_temp[i][j] == -2):
                        try:
                            desk_temp1 = self.checkBlackFoodQueen(desk_temp, i, j)

                            if (desk_temp1 != desk_temp):
                                return desk_temp1
                        except:
                            continue        


        if (self.count % 2):
            if (desk_temp[x1][y1] == 1):

                if (y1 - 1 == y2 and x1 - 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-1][x1-1] = 1
                    if (y2 == 0):
                       desk_temp[y1-1][x1-1] = 2

                if (y1 - 1 == y2 and x1 + 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-1][x1+1] = 1
                    if (y2 == 0):
                       desk_temp[y1-1][x1+1] = 2    

                if (y1 + 1 == y2 and x1 + 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+1][x1+1] = 1
                    if (y2 == 7):
                       desk_temp[y1+1][x1+1] = 2   

                if (y1 + 1 == y2 and x1 - 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+1][x1-1] = 1
                    if (y2 == 7):
                       desk_temp[y1+1][x1+1] = 2                                                                 

                if (y1 - 2 == y2 and x1 - 2 == x2):
                    desk_temp[y1-1][x1-1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-2][x1-2] = 1

                if (y1 - 2 == y2 and x1 + 2 == x2):
                    desk_temp[y1-1][x1+1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-2][x1+2] = 1

                if (y1 + 2 == y2 and x1 + 2 == x2):
                    desk_temp[y1+1][x1+1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+2][x1+2] = 1

                if (y1 + 2 == y2 and x1 - 2 == x2):
                    desk_temp[y1+1][x1-1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+2][x1-2] = 1                    

            elif (desk_temp[x1][y1] == 2):

                if (y1 - 1 == y2 and x1 - 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-1][x1-1] = 2
                    if (y2 == 0):
                       desk_temp[y1-1][x1-1] = 2

                if (y1 - 1 == y2 and x1 + 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-1][x1+1] = 2
                    if (y2 == 0):
                       desk_temp[y1-1][x1+1] = 2    

                if (y1 + 1 == y2 and x1 + 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+1][x1+1] = 2
                    if (y2 == 7):
                       desk_temp[y1+1][x1+1] = 2   

                if (y1 + 1 == y2 and x1 - 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+1][x1-1] = 2
                    if (y2 == 7):
                       desk_temp[y1+1][x1+1] = 2                   

                if (y1 - 2 == y2 and x1 - 2 == x2):
                    desk_temp[y1-1][x1-1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-2][x1-2] = 2

                if (y1 - 2 == y2 and x1 + 2 == x2):
                    desk_temp[y1-1][x1+1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-2][x1+2] = 2

                if (y1 + 2 == y2 and x1 + 2 == x2):
                    desk_temp[y1+1][x1+1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+2][x1+2] = 2

                if (y1 + 2 == y2 and x1 - 2 == x2):
                    desk_temp[y1+1][x1-1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+2][x1-2] = 2 
                 
        else:        
            if (desk_temp[x1][y1] == -1):
                if (y1 - 1 == y2 and x1 - 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-1][x1-1] = -1
                    if (y2 == 0):
                       desk_temp[y1-1][x1-1] = -2

                if (y1 - 1 == y2 and x1 + 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-1][x1+1] = -1
                    if (y2 == 0):
                       desk_temp[y1-1][x1+1] = -2    

                if (y1 + 1 == y2 and x1 + 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+1][x1+1] = -1
                    if (y2 == 7):
                       desk_temp[y1+1][x1+1] = -2   

                if (y1 + 1 == y2 and x1 - 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+1][x1-1] = -1
                    if (y2 == 7):
                       desk_temp[y1+1][x1+1] = -2   


                if (y1 - 2 == y2 and x1 - 2 == x2):
                    desk_temp[y1-1][x1-1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-2][x1-2] = -1

                if (y1 - 2 == y2 and x1 + 2 == x2):
                    desk_temp[y1-1][x1+1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-2][x1+2] = -1

                if (y1 + 2 == y2 and x1 + 2 == x2):
                    desk_temp[y1+1][x1+1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+2][x1+2] = -1

                if (y1 + 2 == y2 and x1 - 2 == x2):
                    desk_temp[y1+1][x1-1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+2][x1-2] = -1

            elif (desk_temp[x1][y1] == -2):
                if (y1 - 1 == y2 and x1 - 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-1][x1-1] = -2
                    if (y2 == 0):
                       desk_temp[y1-1][x1-1] = -2

                if (y1 - 1 == y2 and x1 + 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-1][x1+1] = -2
                    if (y2 == 0):
                       desk_temp[y1-1][x1+1] = -2    

                if (y1 + 1 == y2 and x1 + 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+1][x1+1] = -2
                    if (y2 == 7):
                       desk_temp[y1+1][x1+1] = -2  

                if (y1 + 1 == y2 and x1 - 1 == x2):
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+1][x1-1] = -2
                    if (y2 == 7):
                       desk_temp[y1+1][x1+1] = -2                   

                if (y1 - 2 == y2 and x1 - 2 == x2):
                    desk_temp[y1-1][x1-1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-2][x1-2] = -2

                if (y1 - 2 == y2 and x1 + 2 == x2):
                    desk_temp[y1-1][x1+1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1-2][x1+2] = -2

                if (y1 + 2 == y2 and x1 + 2 == x2):
                    desk_temp[y1+1][x1+1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+2][x1+2] = -2

                if (y1 + 2 == y2 and x1 - 2 == x2):
                    desk_temp[y1+1][x1-1] = 0
                    desk_temp[y1][x1] = 0
                    desk_temp[y1+2][x1-2] = -2 


        self.count += 1 
        self.desk = desk_temp 
        return self.desk

