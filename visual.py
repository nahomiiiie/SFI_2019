import matplotlib.pyplot as plt
import networkx as nx

from mesa.visualization.ModularVisualization import ModularServer
#from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement
from AgeGroup import Individual, Thought, percent_anti, percent_pro


def see_network(G):
    # determines colors of nodes depending on belief pattern
    def node_color(agent):
        return
        {
            Thought.PRO: '#a100ff',
            Thought.ANTI: '#b70101'
        }.get(agent.belief, '#808080')

    def get_agents(source, target):
        return G.node[source]['agent'][0], G.node[target]['agent'][0]

    def visual(self, G):
        nx.draw(G)
        plt.show()


server = ModularServer()
"""
    portrayal = dict()
    portrayal['nodes'] = [{'size': 6,
                           'color': node_color(agents[0])
                           }
                          for (_, agents) in G.nodes.data('agent')]
    portrayal['edges'] = [{'source': source,
                           'target': target
                           }
                          for (source, target) in G.edges]
    return portrayal


# TODO: figure out the actual node visualization, mesa visualization modules

# nx.spring_layout? nx.draw?
# look up for visual
"""
