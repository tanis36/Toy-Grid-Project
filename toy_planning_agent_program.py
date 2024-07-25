from search import Problem, SimpleProblemSolvingAgentProgram, astar_search
from toy_grid import TGState


class ToyGridPickUpProblem(Problem):
    def __init__(self, initial: TGState, goal=None):
        super().__init__(initial, goal)
        self.width = initial.width
        self.height = initial.height
        print('initial problem state')
        initial.display()

    def actions(self, state: TGState):
        cur_loc = state.agent
        acts = ['PickUp']
        left = (cur_loc[0]-1, cur_loc[1])
        right = (cur_loc[0]+1, cur_loc[1])
        up = (cur_loc[0], cur_loc[1]-1)
        down = (cur_loc[0], cur_loc[1]+1)
        if left not in state.obstacles and self.is_inbounds(left):
            acts.append('Left')
        if right not in state.obstacles and self.is_inbounds(right):
            acts.append('Right')
        if up not in state.obstacles and self.is_inbounds(up):
            acts.append('Up')
        if down not in state.obstacles and self.is_inbounds(down):
            acts.append('Down')

        return acts

    def result(self, state: TGState, action: str):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        loc = state.agent

        if action == 'PickUp' and state.agent in state.toys:
            toys = list(state.toys)
            toys.remove(state.agent)
            return TGState(width=state.width, height=state.height, agent=loc,
                           obstacles=state.obstacles, toys=tuple(toys), box=state.box,
                           toys_held=(state.toys_held + 1), capacity=state.capacity)

        new_loc = None
        if action == 'Left':
            new_loc = (loc[0]-1, loc[1])
        elif action == 'Right':
            new_loc = (loc[0]+1, loc[1])
        elif action == 'Up':
            new_loc = (loc[0], loc[1]-1)
        elif action == 'Down':
            new_loc = (loc[0], loc[1]+1)
        else:
            new_loc = (loc[0], loc[1])

        if not self.is_inbounds(new_loc) or new_loc in state.obstacles:
            new_loc = loc

        return TGState(width=state.width, height=state.height, agent=new_loc,
                       obstacles=state.obstacles, toys=state.toys, box=state.box,
                       toys_held=state.toys_held, capacity=state.capacity)

    def goal_test(self, state):
        return len(state.toys) == 0 or state.toys_held == state.capacity

    def is_inbounds(self, loc: tuple[int, int]) -> bool:
        """Check if loc is inside the walls"""
        x, y = loc
        return 0 < x < self.height - 1 and 0 < y < self.width - 1


class ToyGridDropProblem(Problem):
    def __init__(self, initial: TGState, goal=None):
        super().__init__(initial, goal)
        self.width = initial.width
        self.height = initial.height
        print('initial problem state')
        initial.display()

    def actions(self, state: TGState):
        cur_loc = state.agent
        acts = ['Drop']
        left = (cur_loc[0]-1, cur_loc[1])
        right = (cur_loc[0]+1, cur_loc[1])
        up = (cur_loc[0], cur_loc[1]-1)
        down = (cur_loc[0], cur_loc[1]+1)
        if left not in state.obstacles and self.is_inbounds(left):
            acts.append('Left')
        if right not in state.obstacles and self.is_inbounds(right):
            acts.append('Right')
        if up not in state.obstacles and self.is_inbounds(up):
            acts.append('Up')
        if down not in state.obstacles and self.is_inbounds(down):
            acts.append('Down')

        return acts

    def result(self, state: TGState, action: str):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        loc = state.agent

        if action == 'Drop' and state.agent == state.box:
            return TGState(width=state.width, height=state.height, agent=loc,
                           obstacles=state.obstacles, toys=state.toys, box=state.box,
                           toys_held=0, capacity=state.capacity)

        new_loc = None
        if action == 'Left':
            new_loc = (loc[0]-1, loc[1])
        elif action == 'Right':
            new_loc = (loc[0]+1, loc[1])
        elif action == 'Up':
            new_loc = (loc[0], loc[1]-1)
        elif action == 'Down':
            new_loc = (loc[0], loc[1]+1)
        else:
            new_loc = (loc[0], loc[1])

        if not self.is_inbounds(new_loc) or new_loc in state.obstacles:
            new_loc = loc

        return TGState(width=state.width, height=state.height, agent=new_loc,
                       obstacles=state.obstacles, toys=state.toys, box=state.box,
                       toys_held=state.toys_held, capacity=state.capacity)

    def goal_test(self, state):
        return state.toys_held == 0

    def is_inbounds(self, loc: tuple[int, int]) -> bool:
        """Check if loc is inside the walls"""
        x, y = loc
        return 0 < x < self.height - 1 and 0 < y < self.width - 1


class ToyPlanningAgentProgram(SimpleProblemSolvingAgentProgram):
    def __init__(self):
        super().__init__()
        self.h = None

    def update_state(self, percept: TGState):
        # Replace our stored state with the new one. We are assuming that the percept
        # is a full description of the environment
        self.state = percept

    def formulate_problem(self):
        if self.state.toys_held == 0:
            self.h = lambda n: 5*len(n.state.toys)
            return ToyGridPickUpProblem(self.state)
        elif (self.state.toys_held == self.state.capacity or
              (self.state.toys_held < self.state.capacity and len(self.state.toys) == 0)):
            self.h = lambda n: 5*(abs(self.state.agent[0] - self.state.box[0]) + abs(self.state.agent[1] - self.state.box[1]))
            return ToyGridDropProblem(self.state)

    def search(self, problem):
        return astar_search(problem, self.h).solution()

    def show_state(self):
        self.state.display()
