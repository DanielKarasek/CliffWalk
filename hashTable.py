'''
Created on May 17, 2018

@author: danielk
'''

import numpy as np
from copy import copy
from math import *
from Node import Node
        

class Table:
    
    
    def createEmptyArr(self):
        arr = [[] for counter in range(self.size)]
        return arr 
    
    def reset(self):
        self.table = self.createEmptyArr()
    
    
    def newRoot(self,key,done,Qs,getIdx):
        tmpArr = self.createEmptyArr()
        root = self.findKey(key)
        if type(root) != type(None):
            self.addToNewTable(root,tmpArr)
        else:
            root = self.addNode(key = key,done = done, Qs = Qs, getIdx = getIdx,targetTable = tmpArr)
            
        self.table = tmpArr
        return root
        
    
    
    def addToNewTable(self,root,targetTable):
        self.addNode(root = root,targetTable = targetTable)
        
        for node in root.nodes:
            if type(node) != type(None) and type(self.findKey(node.state,targetTable = targetTable)) == type(None):
                self.addToNewTable(node,targetTable = targetTable)

        
        
    def __init__(self,size,hashFunc):
        self.hashFunc = hashFunc
        self.size = size
        self.table = self.createEmptyArr()
        
    
    def findKey(self,key,targetTable = None):
        
        if type(targetTable) == type(None):
            targetTable = self.table

        
        idx = self.hashFunc(key,self.size)
        lenNodes = len(targetTable[idx])
        for counter in range(lenNodes):
            if np.array_equal(targetTable[idx][counter].state, key):
                return targetTable[idx][counter]
        return None 
    
    
    
    def addNode(self,key = None,done = None,Qs = None,getIdx = None,root = None,targetTable = None):
        if type(targetTable) == type(None):
            targetTable = self.table
        
        tmp = type(None)
        
        if type(root) != tmp:
            key = root.state
        
        if type(root) == tmp and (type(key) == tmp or type(done) == tmp or type(Qs) == tmp or type(getIdx) == tmp):
            return None


        node = self.findKey(key,targetTable = targetTable)
        if  type(node) != type(None):
            return node
        elif root == None:
            node = Node(key,done,Qs,getIdx,self)
            idx = self.hashFunc(key,self.size)
            targetTable[idx].append(node)
            return node
        else:
            idx = self.hashFunc(root.state,self.size)
            targetTable[idx].append(root)
            return node
        
            

        
        