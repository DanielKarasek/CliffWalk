import numpy as np
from copy import copy



class Env():
    
    def __init__(self,grid):
        self.grid = grid
        self.size = grid.size
        self.shape = grid.shape
        
        
        ind = np.where(grid==3)
        self.starts_num = len(ind[0])
        self.STARTS = np.column_stack(ind)
        
        self.grid = np.where(grid == 3,0,grid)
        
        self.a_count = 4
        self.restart()

    def setPosition(self,position):
        self.state = copy(position)
        
    def restart(self):
        r = np.random.randint(self.starts_num)
        self.state = copy(self.STARTS[r])
        return copy(self.state)

    def move(self,action):
        old_pos = copy(self.state)
        
        if action == "up":
            self.state[0] -= 1
        elif action == "down":
            self.state[0] += 1
        elif action == "right":
            self.state[1] += 1
        elif action == "left":
            self.state[1] -= 1
        y,x = self.state
        if self.grid[y,x] == 1:
            self.state = old_pos
                

    def step(self,action):
        self.move(action)
        y,x = self.state
        if self.grid[y,x] == 2:
            return copy(self.state),1,True
        else:
            return copy(self.state),0,False
        
        
