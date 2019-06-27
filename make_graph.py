import matplotlib.pyplot as plt
import networkx as nx

from mesa.visualization.ModularVisualization import ModularServer
# from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement


def portray(self, G):
    nx.draw(G, node_color=self.color_map, labels=self.ages, with_labels=True)
    plt.show()

# incorporate joining of networks
