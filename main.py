from toy_grid import ToyGrid
from toy_planning_agent_program import ToyPlanningAgentProgram
from environments import Agent

env = ToyGrid(10,10)
agent = Agent(ToyPlanningAgentProgram())
env.add_thing(agent)
env.run()
print('Final State')
agent.program.show_state()
