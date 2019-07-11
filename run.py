from AgeGroup import IdeaSpread, total_stats
import matplotlib.pyplot as plt
from matplotlib import pylab
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

# py.sign_in('nahomiiie', 'amiraann')
k = 20
t = [1, 2, 3, 4, 5] * k
while k > 0:
    main = IdeaSpread(500, .18, .71, 17, 30)
    main.run(5)
    k -= 1
# print(total_stats)

trace = go.Scatter(
    x=t,
    y=total_stats,
    mode='markers'
)
data = [trace]
layout = go.Layout(title='Anti Vaccine Beliefs in a Population Over Time', xaxis={
                   'title': 'Iteration'}, yaxis={'title': 'Percent of Population'})
plot_url = py.plot(data, filename='26-29')
# mpl_fig = plt.figure()
# this = mpl_fig.subplots()
# this.scatter(t, total_stats)
# this.title()
# unique_url = py.plot_mpl(mpl_fig, filename="20-22")
# py.plot(data, filename="18-19")
