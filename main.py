import Env
import Agent
import numpy as np



grid = np.array(
      [
       [1,1,1,1,1,1,1,1,1,1,1,1],
       [1,3,0,0,0,1,0,0,3,1,2,1],
       [1,3,1,1,0,0,0,0,0,0,0,1],
       [1,3,0,1,3,0,0,0,0,1,0,1],
       [1,0,0,0,0,1,0,0,0,1,0,1],
       [1,0,0,0,3,0,0,0,0,0,2,1],
       [1,1,1,1,1,1,1,1,1,1,1,1],
    ])

lr = 0.8
eps = 0.2

epsDiscount = 0.99
discount = 0.8

dynaPlanLen = 50

useTree = True
keepPlanTree = True
treeSearchLen = 50


e = Env.Env(grid)
a = Agent.Agent(e,eps = eps, lr = lr, epsDiscount = epsDiscount, discount = discount,keepPlan = keepPlanTree, useTree = useTree,treeSearchLen = treeSearchLen)
a.solve(plan_len = dynaPlanLen)
