import math
from enum import Enum
import networkx as nx
import random
import matplotlib.pyplot as plt


from random import sample
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid


class Thought(Enum):
    PRO = 0
    NEUTRAL = 1
    ANTI = 2
# return percentages for pro and anti population


def number_thought(model, thought):
    # creates variable and hold value for number of people with belief
    thought_total = 0
    for x in model.grid.get_all_cell_contents():
        if x.belief is thought:
            thought_total += 1
    return thought_total
    # return sum([1 for a in model.grid.get_all_cell_contents() if a.belief is thought])


def percent_pro(model):
    return (number_thought(model, Thought.PRO))


def percent_anti(model):
    return (number_thought(model, Thought.ANTI))


def percent_neutral(model):
    return (number_thought(model, Thought.NEUTRAL))


class IdeaSpread(Model):
    # creates a set number of agents and has them share beliefs
    # TODO: find out how to create each age group w/ diff params w/o sep models
    def __init__(self, num_nodes=50, avg_node_degree=11, initial_anti=9):
        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        # creates number of nodes and number of connections between each
        self.Vis = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.color_map = []
        # mesa addition, creates knowledge of neighbors
        self.grid = NetworkGrid(self.Vis)
        self.schedule = RandomActivation(self)
        self.initial_anti = initial_anti
        self.datacollector = DataCollector({"Anti Vaxxers": percent_anti,
                                            "Pro Vaxxine": percent_pro})
        # creates agents
        for i, node in enumerate(self.Vis.nodes()):
            a = Individual(i, self, Thought.NEUTRAL)
            self.schedule.add(a)
            self.grid.place_agent(a, node)
            self.color_map.append('green')

            # randomly assigns nodes to be anti within group
            # TODO:figure out random function w nodes
        anti_nodes = random.sample(self.Vis.nodes(), self.initial_anti)
        for a in self.grid.get_cell_list_contents(anti_nodes):
            a.belief = Thought.ANTI
        # set up number that is anti
        # TODO: figure out how to change color of anti po

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run(self, n):
        for i in range(n):
            print(percent_anti(self))
            self.visual(self.Vis)
            self.step()

    def visual(self, G):
        nx.draw(G, node_color=self.color_map, with_labels=True)
        plt.show()


class Individual(Agent):
    def __init__(self, unique_id, model, belief, age=18):
        Agent.__init__(self, unique_id, model)
        self.belief = belief
        self.age = age
        self.pro_friend = 0
        self.anti_friend = 0
    # gives instructions for communicating w neighbors

    def spread_beliefs(self):
        neighbors = [agent for agent in self.model.grid.get_neighbors(
            self.pos, include_center=False)]
        for y in neighbors:
            if y.belief == Thought.ANTI:
                self.anti_friend += 1
            if y.belief == Thought.PRO:
                self.pro_friend += 1
        if self.anti_friend > self.pro_friend:
            self.belief = Thought.ANTI
        elif self.pro_friend > self.anti_friend:
            self.belief = Thought.PRO
        else:
            self.belief = Thought.NEUTRAL

    def step(self):
        self.spread_beliefs()
