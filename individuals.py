import math
from enum import Enum
import networkx as nx

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid


class Thought(Enum):
    PRO = 0
    NEUTRAL = 1
    ANTI = 2


def number_thought(model, state):
    return (sum([1 for a in model.grid.get_all_cell_contents() if a.state is state]))/num_nodes


def percent_pro(model):
    return number_thought(model, Thought.PRO)


def percent_anti(model):
    return number_thought(model, Thought.ANTI)


class Individual(Agent):
    def __init__(self, unique_id, model, intitial_state):
        Agent.__init__(self, unique_id, model)
        self.belief = intitial_state


class IdeaSpread(Model):
    # creates a set number of agents and has them share beliefs
    def __init__(self, num_nodes=50, avg_node_degree=11, initial_anti=(.18)(num_nodes))
    self.num_nodes = num_nodes
