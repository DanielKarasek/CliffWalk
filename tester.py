import Env
import Agent
import numpy as np

e = Env.Env()
a = Agent.Agent(e,eps = 0,lr = 0.01)
a.solve(plan_len = 100)
