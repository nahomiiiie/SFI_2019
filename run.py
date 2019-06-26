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
#from make_graph import see_network
# TODO: fix visualization code, figure out how it works in mesa
#from visual import network_portrayal


main = IdeaSpread(60, 11, .18, 18)
main.run(2)
