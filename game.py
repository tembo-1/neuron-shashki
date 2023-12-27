from perceptron import *
import os

class Game:
    def __init__(self, type : int):
        self.enemy = Perceptron()
        self.enemy.read()
        self.desk = [0] * 9
        self.number = 1
        self.type = type
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
        self.victory = False

    def checkWin(self):
        for i in self.victory_combined:
            if (self.desk[i[0]] == 1 and self.desk[i[1]] == 1 and self.desk[i[2]] == 1):
                return True
            elif (self.desk[i[0]] == -1 and self.desk[i[1]] == -1 and self.desk[i[2]] == -1):
                return True
    
        return False  

    def Print(self):
        os.system('cls')
        print(f"|{self.desk[0]}|{self.desk[1]}|{self.desk[2]}|\n"\
                f"|{self.desk[3]}|{self.desk[4]}|{self.desk[5]}|\n"\
                f"|{self.desk[6]}|{self.desk[7]}|{self.desk[8]}|\n")

    def Check(self):


        if (self.checkWin()):
            if (self.number % 2):
                print('Выиграли нолики')
            else:
                print('Выиграли крестики')    
            self.victory = True
            return  
            
        if (self.number == 10):
            self.victory = True
            print('Ничья')
            return 

    def StepEnemy(self):
        if (self.type == 1):
            self.desk[self.enemy.step(self.desk, self.number)] = -1
            self.number += 1

            self.Print()
            self.Check()
        else:
            self.desk[self.enemy.step(self.desk, self.number)] = 1
            self.number += 1

            self.Print()
            self.Check()
    

    def StepOwn(self, cell : int):
        if (self.desk[cell] != 0):
            return    

        if (self.type == 1):
            self.desk[cell] = 1
            self.number += 1

            self.Print()
            self.Check()

        elif (self.type == -1):
            self.desk[cell] = -1
            self.number += 1

            self.Print()
            self.Check()
