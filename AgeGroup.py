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
    # return float(sum([1 for a in model.population if model.population[a].belief is thought]))/float(len(model.population))
    # ABOVE: the percentage BELOW: the sumb
    return sum([1 for a in model.population if model.population[a].belief is thought])


def percent_pro(model):
    return (number_thought(model, Thought.PRO))


def percent_anti(model):
    return (number_thought(model, Thought.ANTI))


def percent_neutral(model):
    return (number_thought(model, Thought.NEUTRAL))


class IdeaSpread(Model):
    # creates a set number of agents and has them share beliefs
    def __init__(self, num_nodes=50, avg_node_degree=11, initial_anti=.18, initial_pro=.71, age=18):
        self.num_nodes = num_nodes
        prob = float(avg_node_degree) / float(self.num_nodes)
        # creates number of nodes and number of connections between each
        self.color_map = ['gray'] * self.num_nodes
        # mesa addition, creates knowledge of neighbors
        self.schedule = SimultaneousActivation(self)
        self.initial_anti = initial_anti
        self.initial_pro = initial_pro
        # def setup_agents(self, age, num_nodes):
        # creates agents
        self.Vis = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.ages = {}
        self.grid = NetworkGrid(self.Vis)
        self.population = {}

        for i, node in enumerate(self.Vis.nodes()):
            a = Individual(i, self, Thought.NEUTRAL)
            self.schedule.add(a)
            self.grid.place_agent(a, node)
            self.population[a.unique_id] = a
            # randomly assigns nodes to be +/-/0 within group
            if random.random() <= self.initial_anti:
                a.belief = Thought.ANTI
                self.color_map[a.unique_id] = ('red')
            elif random.random() <= self.initial_pro:
                self.color_map[a.unique_id] = 'green'
            else:
                self.color_map[a.unique_id] = 'gray'

        for l in self.population:
            self.ages[l] = self.population[l].age

# TODO: figure otu impletmeentation of datacollector
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
            # reassigns color of people based on belief
            for a in self.population:
                if self.population[a].belief == Thought.ANTI:
                    self.color_map[a] = ('red')
                elif self.population[a].belief == Thought.PRO:
                    self.color_map[a] = 'green'
                else:
                    self.color_map[a] = 'gray'


class Individual(Agent):
    def __init__(self, unique_id, model, belief, age=18):
        Agent.__init__(self, unique_id, model)
        self.unique_id = unique_id
        self.belief = belief
        self.age = age
        self.pro_friend = 0
        self.anti_friend = 0
        self.none = 0
    # gives instructions for communicating w neighbors

    def spread_beliefs(self, population):
        neighbors = [agent for agent in self.model.grid.get_neighbors(
            self.pos, include_center=False)]
        for y in neighbors:
            if population[y].belief == Thought.ANTI:
                self.anti_friend += 1
            if population[y].belief == Thought.PRO:
                self.pro_friend += 1
            if population[y].belief == Thought.NEUTRAL:
                self.none += 1

        if self.anti_friend > self.pro_friend and self.anti_friend > self.none:
            self.belief = Thought.ANTI
        elif self.pro_friend > self.anti_friend and self.pro_friend > self.none:
            self.belief = Thought.PRO
        elif self.none > self.anti_friend and self.none > self.pro_friend:
            self.belief = Thought.NEUTRAL
        else:
            self.belief = Thought.NEUTRAL
        # try and do communtiy based belief change to see if spreads better

    def step(self, population):
        self.spread_beliefs(population)
        # self.advance()

    def advance(self):
        return
