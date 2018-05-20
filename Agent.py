import numpy as np
import graphics
import time
import Env
import tree
from copy import copy

actions = ['up','down','left','right']



class Agent():

    

    def __init__(self,env, lr = 0.03,eps = 0.2,epsDiscount = 0.99,discount = 0.8,keepPlan = True,useTree = True, treeSearchLen = 50):
        
        self.env = env
        self.EnvCopy = copy(env)
        self.size = env.size
        self.env_shape = env.shape
        self.y_s,self.x_s =  self.env_shape
        
        
        self.lr = lr
        self.eps = eps
        self.epsDisc = epsDiscount
        self.discount = discount
        self.a_count = env.a_count
        self.Q = self.qTable()
        self.KnownIdx = np.array([])
        self.TrMem = self.transTable()
        
        self.gr = graphics.Graphics(env.grid,self)
        
        
        
        
        
        self.Tree = tree.Tree(self.EnvCopy,self)
        self.keepPlan = keepPlan
        self.useTree = useTree
        self.treeSearchLen = treeSearchLen

    def qTable(self):
        return np.zeros((self.size,self.a_count))

    def transTable(self):
        TrMem = [x for x in (np.empty((self.size*self.a_count,0,5)))]
        return TrMem
    
    def getIdx(self,state):
        y,x = state
        return int(y*self.x_s + x)

    def getValues(self,state):
        idx = self.getIdx(state)
        return self.Q[idx]

    def getTransIdx(self,state,action):
        y,x = state
        idx = y * self.a_count * self.x_s + x * self.a_count +  action
        return int(idx)
        
        
    def addTrans(self,trans,action_num):
        idx = self.getTransIdx([trans[0],trans[1]],action_num)
        IN_flag = False
        for x in self.TrMem[idx]:
            if np.array_equal(trans,x) == True:
                IN_flag = True
                break
        if IN_flag == False:
            self.TrMem[idx] = np.append(self.TrMem[idx],[trans],axis = 0)
        if self.KnownIdx.__contains__(idx):
            pass
        else:
            self.KnownIdx = np.append(self.KnownIdx,idx)

    def pickTransition(self):
        if self.KnownIdx.size > 0:
            rand = int(np.random.choice(self.KnownIdx))
            a = rand % self.a_count
            transs_len = self.TrMem[rand].shape[0]
            trans_idx = np.random.randint(transs_len)
            trans = self.TrMem[rand][trans_idx]
            return trans,a
        else:
            return 0,0


    def plan(self,steps_count):
        for x in range(steps_count):
            trans,a = self.pickTransition()
            if type (trans)== int:
                print("No transitions available")
                break
            else:
                s,r,s_ = trans[:2],trans[2],trans[3:]
                FormIdx = self.getIdx(s)
                PostIdx = self.getIdx(s_)

                PostMax  = np.amax(self.Q[PostIdx])
                self.Q[FormIdx,a] += self.lr * (r+self.discount*(PostMax)  - self.Q[FormIdx,a])

    def epsPickAction(self,state):
        if np.random.uniform() < self.eps:
            return np.random.randint(self.a_count)
        else:
            return self.pickAction(state)
    
    
    def pickAction(self,state):
        idx = self.getIdx(state)
        m = np.amax(self.Q[idx])
        ind = np.where(self.Q[idx]==m)
        a = np.random.choice(ind[0])
        return a

    def evaluate(self,trans,a):
        s,r,s_ = trans[:2],trans[2],trans[3:]

        FormIdx = self.getIdx(s)
        PostIdx = self.getIdx(s_)

        PostMax  = np.amax(self.Q[PostIdx])
        self.Q[FormIdx,a] += self.lr * (r+self.discount*(PostMax)  - self.Q[FormIdx,a])

    def heuristicTree(self,position,searchLen):
            if np.random.uniform() < self.eps:
                a = np.random.randint(self.a_count)
            else:
                self.EnvCopy.setPosition(position)
                if self.keepPlan == True:
                    self.Tree.changeRoot(position,False)
                else:
                    self.Tree.addNewRoot(position,False)
                a = self.Tree.MonteCarloTreeSearch(searchLen)
            return a
    
    
    def takeAction(self,s):
        if self.useTree == True:
            a = self.heuristicTree(s, self.treeSearchLen)
        else:
            a = self.epsPickAction(s)
        return a


    def solve(self,episodes = 3000,plan_len = 10):
        samePosCounter = 0
        for epNum in range(episodes):
            s = self.env.restart()
            steps = 0
            done = False
            self.gr.drawMap()
            self.gr.drawAgent(s)
            self.gr.update()
            while not done:
                steps += 1
                
                a = self.takeAction(s)
                
                s_,r,done = self.env.step(actions[a])
                trans = [s[0],s[1],r,s_[0],s_[1]]

                
                self.addTrans(trans,a)
                
                self.evaluate(trans,a)
                self.plan(plan_len)
                
                if np.array_equal(s, s_):
                    samePosCounter += 1
                else:
                    samePosCounter = 0
                
                s = s_            

                self.gr.drawMap()
                self.gr.drawAgent(s_)
                self.gr.update()
                time.sleep(0.01)

            self.Tree.reset()
            print(steps)
            self.eps *= self.epsDisc
        
        

