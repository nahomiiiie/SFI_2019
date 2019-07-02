# insert parameters for run
# wrtie, read file, come from command line
# add everythign from file, same sequence of things
# plot ot file and add? matplotlib
"""
import math
from enum import Enum
import networkx as nx

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
"""
from AgeGroup import IdeaSpread

main = IdeaSpread(100, .18, .71, 18, 22)

main.run(2)
