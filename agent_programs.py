import random
from environments import Agent, loc_A, loc_B


def trace_agent(agent):
    """Wrap the agent's program to print its input and output. This will let
    you see what the agent is doing in the environment."""
    old_program = agent.program

    def new_program(percept):
        action = old_program(percept)
        print('{} perceives {} and does {}'.format(agent, percept, action))
        return action

    agent.program = new_program
    return agent


def table_driven_agent(table):
    """
    [Figure 2.7]
    This agent selects an action based on the percept sequence.
    It is practical only for tiny domains.
    To customize it, provide as table a dictionary of all
    {percept_sequence:action} pairs.
    """
    percepts = []

    def program(percept):
        percepts.append(percept)
        action = table.get(tuple(percepts))
        return action

    return program


def random_agent(actions):
    """An agent that chooses an action at random, ignoring all percepts.
         list = ['Right', 'Left', 'Suck', 'NoOp']
         program = random_agent(list)
         agent = Agent(program)
         environment = TrivialVacuumEnvironment()
         environment.add_thing(agent)
         environment.run()
         environment.status == {(1, 0): 'Clean' , (0, 0): 'Clean'}
    True
    """
    return lambda percept: random.choice(actions)


def simple_reflex_agent(rules, interpret_input):
    """
    [Figure 2.10]
    This agent takes action based solely on the percept.
    """

    def program(percept):
        state = interpret_input(percept)
        rule = rule_match(state, rules)
        action = rule.action
        return action

    return program


def model_based_reflex_agent(rules, update_state, transition_model, sensor_model):
    """
    [Figure 2.12]
    This agent takes action based on the percept and state.
    """

    def program(percept):
        program.state = update_state(program.state, program.action, percept, transition_model, sensor_model)
        rule = rule_match(program.state, rules)
        action = rule.action
        return action

    program.state = program.action = None
    return program


def rule_match(state, rules):
    """Find the first rule that matches state."""
    for rule in rules:
        if rule.matches(state):
            return rule


def random_vacuum_agent():
    """Randomly choose one of the actions from the vacuum environment.
         agent = random_vacuum_agent()
         environment = TrivialVacuumEnvironment()
         environment.add_thing(agent)
         environment.run()
         environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """
    return Agent(random_agent(['Right', 'Left', 'Suck', 'NoOp']))


def table_driven_vacuum_agent():
    """Tabular approach towards vacuum world as mentioned in [Figure 2.3]
         agent = table_driven_vacuum_agent()
         environment = TrivialVacuumEnvironment()
         environment.add_thing(agent)
         environment.run()
         environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """
    table = {((loc_A, 'Clean'),): 'Right',
             ((loc_A, 'Dirty'),): 'Suck',
             ((loc_B, 'Clean'),): 'Left',
             ((loc_B, 'Dirty'),): 'Suck',
             ((loc_A, 'Dirty'), (loc_A, 'Clean')): 'Right',
             ((loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean')): 'Left',
             ((loc_A, 'Dirty'), (loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck'}
    return Agent(table_driven_agent(table))


def reflex_vacuum_agent():
    """
    [Figure 2.8]
    A reflex agent for the two-state vacuum environment.
        agent = reflex_vacuum_agent()
        environment = TrivialVacuumEnvironment()
        environment.add_thing(agent)
        environment.run()
        environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """

    def program(percept):
        location, status = percept
        if status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'

    return Agent(program)


def model_based_vacuum_agent():
    """An agent that keeps track of what locations are clean or dirty.
         agent = model_based_vacuum_agent()
         environment = TrivialVacuumEnvironment()
         environment.add_thing(agent)
         environment.run()
         environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """
    model = {loc_A: None, loc_B: None}

    def program(percept):
        """Same as ReflexVacuumAgent, except if everything is clean, do NoOp."""
        location, status = percept
        model[location] = status  # Update the model here
        if model[loc_A] == model[loc_B] == 'Clean':
            return 'NoOp'
        elif status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'

    return Agent(program)
