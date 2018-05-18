import tree
import Queue
import numpy as np

class Env:
    def __init__(self):
        pass


    def step(self,x):
        rand = np.random.randint(5)-2
        return [2,1],rand,False



env = Env()
Que = Queue.Queue()
node = tree.Node([1,1],False)
tree = tree.Tree(env,None,node)

for x in range(10):
    tree.findBestWay()



