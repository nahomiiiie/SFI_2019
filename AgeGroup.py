import math
from enum import Enum
import networkx as nx
import random
import matplotlib.pyplot as plt


from random import sample
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
from make_graph import portray


class Thought(Enum):
    PRO = 0
    NEUTRAL = 1
    ANTI = 2
# return percentages for pro and anti population


def number_thought(model, thought):
    # creates variable and hold value for number of people with belief
    #thought_total = 0
    # for x in model.grid.get_all_cell_contents():
    #    if x.belief is thought:
     #       thought_total += 1
    # return thought_total
    return sum([1 for a in model.population if model.population[a].belief is thought])


def percent_pro(model):
    return (number_thought(model, Thought.PRO))


def percent_anti(model):
    return (number_thought(model, Thought.ANTI))


def percent_neutral(model):
    return (number_thought(model, Thought.NEUTRAL))


class IdeaSpread(Model):
    # creates a set number of agents and has them share beliefs
    # TODO: find out how to create each age group w/ diff params w/o sep models
    def __init__(self, num_nodes=50, avg_node_degree=11, initial_anti=.18, age=18):
        self.num_nodes = num_nodes
        prob = float(avg_node_degree) / float(self.num_nodes)
        # creates number of nodes and number of connections between each
        self.color_map = ['gray'] * self.num_nodes
        # mesa addition, creates knowledge of neighbors
        self.schedule = SimultaneousActivation(self)
        self.initial_anti = initial_anti
        # def setup_agents(self, age, num_nodes):
        # creates agents
        self.Vis = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = NetworkGrid(self.Vis)
        self.population = {}

        for i, node in enumerate(self.Vis.nodes()):
            a = Individual(i, self, Thought.NEUTRAL)
            self.schedule.add(a)
            self.grid.place_agent(a, node)
            self.population[a.unique_id] = a
            # randomly assigns nodes to be anti within group
            if random.random() <= self.initial_anti:
                a.belief = Thought.ANTI
                self.color_map[a.unique_id] = ('red')
            else:
                self.color_map[a.unique_id] = 'green'

        # set up number that is anti
        # TODO: figure out how to change color of anti po

        self.datacollector = DataCollector({"Anti Vaxxers": percent_anti,
                                            "Pro Vaxxine": percent_pro})
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step(self.population)
        self.datacollector.collect(self)
# TODO: when run, do not set up new networks

    def run(self, n):
        for i in range(n):
            print(percent_anti(self))
            portray(self, self.Vis)
            self.step()
            for a in self.population:
                if self.population[a].belief == Thought.ANTI:
                    self.color_map[a] = ('red')
                else:
                    self.color_map[a] = 'green'


class Individual(Agent):
    def __init__(self, unique_id, model, belief, age=18):
        Agent.__init__(self, unique_id, model)
        self.unique_id = unique_id
        self.belief = belief
        self.age = age
        self.pro_friend = 0
        self.anti_friend = 0
    # gives instructions for communicating w neighbors

    def spread_beliefs(self, population):
        neighbors = [agent for agent in self.model.grid.get_neighbors(
            self.pos, include_center=False)]
        for y in neighbors:
            if population[y].belief == Thought.ANTI:
                self.anti_friend += 1
            if population[y].belief == Thought.PRO:
                self.pro_friend += 1

        # changing
        # TODO: incorporate the neutral mindest in determining
        if self.anti_friend > self.pro_friend:
            self.belief = Thought.ANTI
        # elif self.pro_friend > self.anti_friend:
        #    self.belief = Thought.PRO

        else:
            self.belief = Thought.NEUTRAL

    def step(self, population):
        self.spread_beliefs(population)
        # self.advance()

    def advance(self):
        return


# save location as dict pos = {},networkx for edges8
