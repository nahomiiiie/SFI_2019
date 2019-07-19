import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import pylab

import plotly.plotly as py
import plotly.express as px


from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement


def portray(self, G):
    nx.draw(G, node_color=self.color_map, labels=self.ages, with_labels=True)
    plt.show()


"""
class MyFigure(Figure):
    def __init__(self, figtitle, *args, **kwargs):

custom kwarg figtitle is a figure title
        Figure.__init__(*args, **kwargs)
        self.text(0.5, 0.95, figtitle, ha='center')
"""
# incorporate joining of networks
