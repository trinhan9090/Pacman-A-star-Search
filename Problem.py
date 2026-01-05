class Node:
    def __init__(self, pac, food_left, pies_left, action = None, Parent = None):
        self.pac = pac #pacman position, tuple, pac-man position will be store as (pos_y, pox_x) to follow the rule of 2d list
        self.foods = tuple(food_left) # a tuple store all position of remaining foods
        self.pie = tuple(pies_left) # a tuple to store all position of remaining pies
        self.action = action # takes action to make new node
        self.parent = Parent
        self.power = 0
        self.f = 0
        self.g = 0

    def __eq__(self, other): 
        return self.pac == other.pac and self.foods == other.foods
    def __hash__(self): 
        return hash((self.pac, self.foods))
    def __lt__(self, other):
        return self.f < other.f
    
    def setParent(self, parent):    
        self.parent = parent
    def setF(self, f):
        self.f = f
    def setG(self, g):
        self.g = g
    def setPower(self, p):
        self.power = p
    
    def getParent(self):
        return self.parent
    def getF(self):
        return self.f
    def getG(self):
        return self.g
    def getAction(self):
        return self.action
    def getPosition(self):
        return self.pac
    def getFoods(self):
        return self.foods
    def getPie(self):
        return self.pie


class Graph():
    def __init__(self):
        self.grid = [] # environment, map of the game
        self.pacman = None # agent
        self.foods = [] # foods
        self.pies = [] # pies

    def load_map(self,filepath):
        with open(filepath,'r') as file:
            for y, line in enumerate(file.readlines()):
                row = []
                for x, char in enumerate(line.strip()):
                    if char == 'P':
                        self.pacman = (y,x)
                    elif char == '.':
                        self.foods.append((y, x))
                    elif char == 'O':
                        self.pies.append((y, x))
                    row.append(char)
                self.grid.append(row)
            return self.grid # 2d list
    
    def get_pacman(self):
        return self.pacman
    def get_grid(self ):
        return self.grid
    def get_foods(self):
        return self.foods
    def get_pies(self):
        return self.pies