import math
from enum import Enum
import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

from random import sample
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
from make_graph import portray

probabilities = {}
groupsize = [21.8, 15.0, 14.3, 13.9]

talk = [11.1, 1.6, .8, .6, 2.6, 4.3, 1.7,
        1.1, .9, 2.0, 3.4, 1.8, .5, 1.0, 1.7, 2.7]
total_stats = []


class Thought(Enum):
    PRO = 0
    NEUTRAL = 1
    ANTI = 2

# return percentages for pro and anti population


def number_thought(model, thought):
    return float(sum([1 for a in model.population if model.population[a].belief is thought]))/float(len(model.population)) * 100
    # ABOVE: the percentage BELOW: the sum
    # return sum([1 for a in model.population if model.population[a].belief is thought])


def percent_pro(model):
    return (number_thought(model, Thought.PRO))


def percent_anti(model):
    return (number_thought(model, Thought.ANTI))


def percent_neutral(model):
    return (number_thought(model, Thought.NEUTRAL))


class IdeaSpread(Model):
    # creates a set number of agents and has them share beliefs
    def __init__(self, num_nodes=50, initial_anti=.18, initial_pro=.71, first_age=18, last_age=22):
        self.color_map = ['gray'] * num_nodes
        # mesa addition, creates knowledge of neighbors
        self.schedule = SimultaneousActivation(self)
        self.initial_anti = initial_anti
        self.initial_pro = initial_pro
        self.Vis = nx.Graph()
        self.Vis.add_nodes_from(range(num_nodes))
        self.ages = {}
        self.grid = NetworkGrid(self.Vis)
        self.population = {}
        # creates nodes with unique id, netural and makes equal number of each age
        for i, node in enumerate(self.Vis.nodes()):
            a = Individual(i, self, Thought.NEUTRAL, first_age +
                           i*(last_age - first_age)/num_nodes)
            self.schedule.add(a)
            self.grid.place_agent(a, node)
            self.population[a.unique_id] = a
            # initializes percent of population w anti/pro and remainder neutral. sets color of belief
            if random.random() <= self.initial_anti:
                a.belief = Thought.ANTI
                self.color_map[a.unique_id] = ('red')
            elif random.random() <= self.initial_pro:
                a.belief = Thought.PRO
                self.color_map[a.unique_id] = 'green'
            else:
                self.color_map[a.unique_id] = 'gray'

        # adds age to dictionary with unique id
        for l in self.population:
            self.ages[l] = self.population[l].age

        # assigns edges (connections) between people
        for id1 in self.population:
            for id2 in self.population:
                if self.population[id1].prob_ref == 0 and id1 < id2:
                    if self.population[id2].prob_ref == 0 and random.random() < (talk[0]/groupsize[0]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 1 and random.random() < (talk[1]/groupsize[0]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 2 and random.random() < (talk[2]/groupsize[0]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 3 and random.random() < (talk[3]/groupsize[0]):
                        self.Vis.add_edge(id1, id2)
                if self.population[id1].prob_ref == 1 and id1 < id2:
                    if self.population[id2].prob_ref == 0 and random.random() < (talk[4]/groupsize[1]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 1 and random.random() < (talk[5]/groupsize[1]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 2 and random.random() < (talk[6]/groupsize[1]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 3 and random.random() < (talk[7]/groupsize[1]):
                        self.Vis.add_edge(id1, id2)
                if self.population[id1].prob_ref == 2 and id1 < id2:
                    if self.population[id2].prob_ref == 0 and random.random() < (talk[8]/groupsize[2]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 1 and random.random() < (talk[9]/groupsize[2]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 2 and random.random() < (talk[10]/groupsize[2]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 3 and random.random() < (talk[11]/groupsize[2]):
                        self.Vis.add_edge(id1, id2)
                if self.population[id1].prob_ref == 3 and id1 < id2:
                    if self.population[id2].prob_ref == 0 and random.random() < (talk[12]/groupsize[3]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 1 and random.random() < (talk[13]/groupsize[3]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 2 and random.random() < (talk[14]/groupsize[3]):
                        self.Vis.add_edge(id1, id2)
                    if self.population[id2].prob_ref == 3 and random.random() < (talk[15]/groupsize[3]):
                        self.Vis.add_edge(id1, id2)

        self.datacollector = DataCollector({"Anti Vaxxers": percent_anti,
                                            "Pro Vaxxine": percent_pro})
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step(self.population, self.Vis)
        self.datacollector.collect(self)

    def run(self, n):
        i = 1
        while i <= n:
            print(percent_anti(self))
            total_stats.append(percent_anti(self))
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
            i += 1


class Individual(Agent):
    def __init__(self, unique_id, model, belief, age=18):
        Agent.__init__(self, unique_id, model)
        self.unique_id = unique_id
        self.belief = belief
        self.age = age
        self.pro_friend = 0.0
        self.anti_friend = 0.0
        self.none = 0.0
        if self.age <= 19:
            self.prob_ref = 0
        elif self.age <= 24:
            self.prob_ref = 1
        elif self.age <= 29:
            self.prob_ref = 2
        else:
            self.prob_ref = 3

    # gives instructions for communicating w neighbors
    # CURRENT: each friend has sam
    def spread_beliefs(self, population, G):
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

# recognizes friends and goes in to

    def switch_friends(self, population, G):
        # print(self.none, self.pro_friend,
              # self.anti_friend, self.belief, self.unique_id)
        neighbors = G[self.unique_id]
        # print(G.node[shoop]["agent"][0].belief)

        # finds first neighbor with diff belief and removes the edge
        for n in neighbors:
            i = 0
            # print(n)
            if G.nodes[n]["agent"][0].belief != self.belief:
                G.remove_edge(self.unique_id, n)
                # np.random.shuffle(list(G))
                j = random.randint(0, 99)
                # IMPORTANT: change 99 depending on popualtion size
                if G.nodes[j]["agent"][0].belief == self.belief:
                    G.add_edge(self.unique_id, j)
                    break
                else:
                    j = random.randint(0, 99)
                break
            i += 1

    def step(self, population, graph):
        print(self.none, self.pro_friend,
              self.anti_friend, self.belief, self.unique_id)
        self.spread_beliefs(population, graph)
        self.switch_friends(population, graph)
        # self.advance()

    def advance(self):
        return
