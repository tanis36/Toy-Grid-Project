# Toy-Grid-Project
This was a project for an Artificial Intelligence class. The goal of this project was to take an existing vacuum grid project, where a vacuum agent performs A* search to find the optimal path to clean all dirt on the floor, and modify it so that we have an agent that uses A* search to find all the toys on the floor and return them to a toy box. There are two versions of this project: one where the agent has no carrying capacity, and another where the agent is limited to the number of toys it can carry. In the first version mentioned, the agent will pick up all the toys on the floor and then find the toy box to drop them into. In the second version, after the agent picks up its carrying capacity, it must find the toy box and drop the toys before it can go searching for more. Both verisons can be seen by adjusting the self.capacity variable in the Agent class found in environments.py. This project was constructed so that instead of having the agent find the toys and go to the toy box to drop them be one single search problem, there are two search problems: one for finding toys and another for finding the toy box. While the agent may not find the most optimal path from start to finsih, this allows the agent to handle much larger state spaces, as there are less total states to consider.
