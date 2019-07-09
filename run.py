
from AgeGroup import IdeaSpread, total_stats
import matplotlib.pyplot as plt
import numpy as np

k = 5
t = [1, 2, 3, 4, 5] * k
while k > 0:
    main = IdeaSpread(100, .18, .71, 18, 30)
    main.run(5)
    k -= 1
# print(total_stats)
plt.scatter(t, total_stats, color='#9872ab')
#plt.scatter(t, total_stats19)
# ^^^continue for all ages to put on same graph
plt.xticks(np.arange(1, 6, step=1))
plt.yticks(np.arange(0, 20, step=1))
plt.xlabel('Iteration')
plt.ylabel('Percent of population')
plt.title('Anti Vaccine Beliefs in a Population Over Time')
plt.savefig("18year_anti.pdf")
plt.show()
