'''
Created on May 17, 2018

@author: danielk
'''

import numpy as np
from copy import copy
from math import *



action = ["up","down","left","right"]        
        


class Node:

    def __init__(self,state,done,Qs,getIdx,table):
        self.getIdx = getIdx
        self.Qs = Qs
        self.state = state
        self.done = done
        self.table = table
        self.values = [0,0]      ##denominator at 0 nominator at 1 
        self.actionRewards = [None,None,None,None]
        self.nodes = [None,None,None,None]
    

    def isInNodes(self,action):
        if self.nodes[action] == None:
            return False
        else:
            return True

    def addNode(self,action,node):
        self.nodes[action] = node
    

    def getRatios(self):
        ratios = np.zeros(4)
        rewards = [rew if rew is not None else 0 for rew in self.actionRewards]
        for node,idx in zip(self.nodes,range(len(self.nodes))):
            if node is not None:
                
                if not node.done:
                    ratios[idx] = node.values[1]/node.values[0] +  sqrt(2)*sqrt((log(self.values[0]+1))/node.values[0]) + rewards[idx]
                else:
                    ratios[idx] = 1 + sqrt(2)*sqrt(log(self.values[0]+1)/node.values[0])
            else:
                ratios[idx] = self.Qs[self.getIdx(self.state),idx] + sqrt(2)*sqrt(log(self.values[0]+1)/1)
        return ratios
    
    def getRawRatios(self):
        ratios = np.zeros(4)
        rewards = [rew if rew is not None else 0 for rew in self.actionRewards]
        for node,idx in zip(self.nodes,range(len(self.nodes))):
            if node is not None:    
                ratios[idx] = node.values[1]/node.values[0] + rewards[idx]

            else:
                ratios[idx] = self.Qs[self.getIdx(self.state),idx]
        return ratios
    
    def getChoice(self,pFlag = 0,getAFlag = 0):
        
        if getAFlag == 0:
            ratios = self.getRatios()
        elif getAFlag == 1:
            ratios = self.getRawRatios()
        else:
            print("error, returned 0 ")
            return 0
        #ratios += self.Qs[self.getIdx(self.state)]
        maxim = np.amax(ratios)
        indices = np.where(ratios == maxim)
        choice = np.random.choice(indices[0])
        if pFlag == 1:
            print("state is:",self.state)
            print("ratios:",ratios)
            print("chosen is: ",action[choice])
            print("xxxxxxxxxxxxxxxx")
        return choice

    def findBest(self,Que,env,discount,counter = 0):
        
        choice = self.getChoice()
        Que.push(self)
        
        if self.done:
            return copy(self.state),0,True
        if counter > 50:
            return copy(self.state),0,self.done
        
        if not self.isInNodes(choice):
            env.setPosition(self.state)
            s_,r,done = env.step(action[choice])
            s_ = copy(s_)
            
            self.actionRewards[choice] = r
            self.values[1] += r
            r *= discount
            
            n = self.table.addNode(s_,done,self.Qs,self.getIdx)
            self.addNode(choice,n)
            Que.push(n)
            
            return copy(s_),r,done

        elif not self.done:
            s_,r ,done = self.nodes[choice].findBest(Que,env,discount,counter = counter +1)
            s_ = copy(s_)
            r += self.actionRewards[choice]
            self.values[1] += r
            r *= discount
            return copy(s_),r,done
        
        
        
            
        

class Table:
    
    
    def createArr(self,size):
        arr = [[] for counter in range(size)]
        return arr 
    
    def __init__(self,size,hashFunc):
        self.table = self.createArr(size)
        self.hashFunc = hashFunc
        self.size = size
    
    def findKey(self,key):
        idx = self.hashFunc(key,self.size)
        lenNodes = len(self.table[idx])
        for counter in range(lenNodes):
            if np.array_equal(self.table[idx][counter].state, key):
                return self.table[idx][counter]
        return None 
    
    def addNode(self,key,done,Qs,getIdx):
        node = self.findKey(key)
        if  type(node) != type(None):
            return node
        else:
            node = Node(key,done,Qs,getIdx,self)
            idx = self.hashFunc(key,self.size)
            self.table[idx].append(node)
            return node
        
            

        
        