import Env
import Agent
import numpy as np



eps = 0.2
discount = 0.8
lr = 0.01
epsDiscount = 0.99

useTree = True
keepPlanTree = True
treeSearchLen = 50


e = Env.Env()
a = Agent.Agent(e,eps = eps, lr = lr, epsDiscount = epsDiscount, discount = discount,keepPlan = keepPlanTree, useTree = useTree,treeSearchLen = treeSearchLen)
a.solve(plan_len = 100)
