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

probabilities = {}
probabilities[0] = 21.8
probabilities[1] = 15.0
probabilities[2] = 14.3
probabilities[3] = 13.9

talk = [11.1, 1.6, .8, .6, 2.6, 4.3, 1.7,
        1.1, .9, 2.0, 3.4, 1.8, .5, 1.0, 1.7, 2.7]


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
    def __init__(self, num_nodes=50, initial_anti=.18, initial_pro=.71, first_age=18, last_age=22):
        self.num_nodes = num_nodes
        #prob = float(avg_node_degree) / float(self.num_nodes)
        # creates number of nodes and number of connections between each
        self.color_map = ['gray'] * self.num_nodes
        # mesa addition, creates knowledge of neighbors
        self.schedule = SimultaneousActivation(self)
        self.initial_anti = initial_anti
        self.initial_pro = initial_pro
        # def setup_agents(self, age, num_nodes):
        # creates agents
        self.Vis = nx.Graph()
        self.Vis.add_nodes_from(range(num_nodes))
        self.ages = {}
        self.grid = NetworkGrid(self.Vis)
        self.population = {}

        for i, node in enumerate(self.Vis.nodes()):
            a = Individual(i, self, Thought.NEUTRAL, first_age +
                           i*(last_age - first_age)/num_nodes)
            self.schedule.add(a)
            self.grid.place_agent(a, node)
            self.population[a.unique_id] = a
            # randomly assigns nodes to be +/-/0 within group
            if random.random() <= self.initial_anti:
                a.belief = Thought.ANTI
                self.color_map[a.unique_id] = ('red')
            elif random.random() <= self.initial_pro:
                a.belief = Thought.PRO
                self.color_map[a.unique_id] = 'green'
            else:
                self.color_map[a.unique_id] = 'gray'
        #invest in matrix

        for id1 in self.population:
            for id2 in self.population:
                if self.population[id1].prob_ref == 0:
                    if id1 < id2 and self.population[id2].prob_ref == 0 and random.random() < (talk[0]/probabilities[0]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 1 and random.random() < (talk[1]/probabilities[0]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 2 and random.random() < (talk[2]/probabilities[0]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 3 and random.random() < (talk[3]/probabilities[0]):
                        self.Vis.add_edge(id1, id2)
                if self.population[id1].prob_ref == 1:
                    if id1 < id2 and self.population[id2].prob_ref == 0 and random.random() < (talk[4]/probabilities[1]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 1 and random.random() < (talk[5]/probabilities[1]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 2 and random.random() < (talk[6]/probabilities[1]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 3 and random.random() < (talk[7]/probabilities[1]):
                        self.Vis.add_edge(id1, id2)
                if self.population[id1].prob_ref == 2:
                    if id1 < id2 and self.population[id2].prob_ref == 0 and random.random() < (talk[8]/probabilities[2]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 1 and random.random() < (talk[9]/probabilities[2]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 2 and random.random() < (talk[10]/probabilities[2]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 3 and random.random() < (talk[11]/probabilities[2]):
                        self.Vis.add_edge(id1, id2)
                if self.population[id1].prob_ref == 3:
                    if id1 < id2 and self.population[id2].prob_ref == 0 and random.random() < (talk[12]/probabilities[3]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 1 and random.random() < (talk[13]/probabilities[3]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 2 and random.random() < (talk[14]/probabilities[3]):
                        self.Vis.add_edge(id1, id2)
                    if id1 < id2 and self.population[id2].prob_ref == 3 and random.random() < (talk[15]/probabilities[3]):
                        self.Vis.add_edge(id1, id2)


# TODO: change prob of connection bwn ages groups

        for l in self.population:
            self.ages[l] = self.population[l].age


# TODO: figure out implementation of datacollector
        self.datacollector = DataCollector({"Anti Vaxxers": percent_anti,
                                            "Pro Vaxxine": percent_pro})
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step(self.population, self.Vis)
        self.datacollector.collect(self)

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
        if self.age <= 19:
            self.prob_ref = 0
        elif self.age <= 24:
            self.prob_ref = 1
        elif self.age <= 29:
            self.prob_ref = 2
        else:
            self.prob_ref = 3
    # gives instructions for communicating w neighbors

    def spread_beliefs(self, population, G):
        # TODO: check who has edges
        # self.Vis[x] for x in self.population
        # neighbors = [agent for agent in self.model.grid.get_neighbors(
            # self.pos, include_center = False)]
        neighbors = G[self.unique_id]
        self.pro_friend = 0
        self.anti_friend = 0
        self.none = 0
        for y in neighbors:
            if population[y].belief == Thought.ANTI:
                self.anti_friend += 1
            if population[y].belief == Thought.PRO:
                self.pro_friend += 1
            if population[y].belief == Thought.NEUTRAL:
                self.none += 1

        if self.pro_friend > self.anti_friend and self.pro_friend > self.none:
            self.belief = Thought.PRO
        elif self.anti_friend > self.pro_friend and self.anti_friend > self.none:
            self.belief = Thought.ANTI

        elif self.none > self.anti_friend and self.none > self.pro_friend:
            self.belief = Thought.NEUTRAL
        else:
            self.belief = self.belief
        #print(self.none, self.pro_friend, self.anti_friend, self.belief)
        # try and do communtiy based belief change to see if spreads better

    def step(self, population, graph):
        self.spread_beliefs(population, graph)
        # self.advance()

    def advance(self):
        return
