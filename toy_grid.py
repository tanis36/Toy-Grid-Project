
from environments import XYEnvironment, Wall, Obstacle, Toy, Box, Agent
import random
from dataclasses import dataclass
import os
from time import sleep


@dataclass(frozen=True, order=True)
class TGState:
    width: int
    height: int
    agent: tuple[int, int]
    obstacles: tuple[tuple[int, int], ...]
    toys: tuple[tuple[int, int], ...]
    box: tuple[int, int]
    toys_held: int
    capacity: int

    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.agent:
                    print('A', end=" ")
                elif (x, y) == self.box:
                    print('B', end=" ")
                elif (x, y) in self.obstacles:
                    print('C', end=" ")
                elif (x, y) in self.toys:
                    print('T', end=" ")
                elif x == 0 or x == self.width - 1:
                    print('|', end=" ")
                elif y == 0 or y == self.height - 1:
                    print('-', end=" ")
                else:
                    print('.', end=" ")
            print()
        print(f'Agent is holding {self.toys_held} toys.')


class ToyGrid(XYEnvironment):
    def __init__(self, width, height, toys=25):
        super().__init__(width, height)

        # walls around the exterior
        self.add_walls()

        # arrange some obstacles.
        for i in range(1, width // 2):
            self.add_thing(Obstacle(), (i, 3))
            self.add_thing(Obstacle(), (width - i - 1, height - 4))

        # add a box
        self.add_thing(Box(), (random.randrange(1, width - 1), random.randrange(1, height - 1)), empty_only=True)

        # toss in some toys
        for _ in range(toys):
            self.add_thing(Toy(), (random.randrange(1, width - 1), random.randrange(1, height - 1)), empty_only=True)

    def thing_classes(self):
        return [Wall, Toy, Box, Obstacle, Agent]

    def percept(self, agent):
        # the agent can see the entire environment. How does this work:
        return TGState(width=self.width, height=self.height,
                       agent=self.agents[0].location,
                       obstacles=tuple([o.location for o in self.things if isinstance(o, Obstacle)]),
                       toys=tuple([t.location for t in self.things if isinstance(t, Toy)]),
                       box=[b.location for b in self.things if isinstance(b, Box)][0],
                       toys_held=self.agents[0].holding,
                       capacity=self.agents[0].capacity)

    def execute_action(self, agent, action):
        if action == 'PickUp':
            toy_list = self.list_things_at(agent.location, Toy)
            if agent.holding < agent.capacity:
                if toy_list:
                    toy = toy_list[0]
                    agent.performance += 1
                    agent.holding += 1
                    self.delete_thing(toy)
        elif action == 'Drop':
            box_list = self.list_things_at(agent.location, Box)
            if (agent.holding == agent.capacity or
                    (agent.holding < agent.capacity and len([t for t in self.things if isinstance(t, Toy)]) == 0)):
                if box_list:
                    agent.performance += 1
                    agent.holding = 0
        else:
            new_loc = None
            if action == 'Left':
                new_loc = (agent.location[0]-1, agent.location[1])
            elif action == 'Right':
                new_loc = (agent.location[0]+1, agent.location[1])
            elif action == 'Up':
                new_loc = (agent.location[0], agent.location[1]-1)
            elif action == 'Down':
                new_loc = (agent.location[0], agent.location[1]+1)

            if new_loc and (not self.some_things_at(new_loc, Obstacle)
                            and not self.some_things_at(new_loc, Wall)):
                agent.location = new_loc

    def is_done(self):
        return len([t for t in self.things if isinstance(t, Toy)]) == 0 and self.agents[0].holding == 0

    def display(self, s, action):
        sleep(0.5)
        os.system('clear')
        print(f'step {s}: action {action}')
        self.agents[0].program.show_state()
