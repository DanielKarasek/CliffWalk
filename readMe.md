# Cliff walk
This is implementation of Dyna-Q and Monte Carlo Tree Search(MCTS) on grid world.

Parameters in main:
grid :

	map of the grid world. Each number has different meaning. 
	1 - wall
	2 - goal
	3 - start position
	4 - normal square on which agent can step
	World has to include walls at sides and at least one goal and start
	but more of them can be included

lr:
	learning rate for TD updates
	values: [0,1] for dyna-Q we can use numbers closer to 1

eps:
	exploration parameter. We take the best known action with probability 1-eps and random
	action with probability eps
	values: [0,1] usually close to zero or decayed faster

epsDiscount: 
	influence speed of eps decay
	values: [0,1] usually close to 1

discount:
	regulazation parameter used for TD updates. Later rewards are lowered by power of this 
	number
	values: [0,1] usually close to 1

dynaPlanLen:
	Number of transition that will be used to plan via dyna planning strategy
	values: <0,inf> (zero effectivelly shut down whole planning process)

useTree:
	boolean defining whether to use MCTS or not
	values: <True,False>

keepPlanTree:
	boolean defining whether we can use values from previous search or restart whole search 
	after each action taken
	values: <True,False>

treeSearchLen:
	How many nodes can Tree (graph) contain 
