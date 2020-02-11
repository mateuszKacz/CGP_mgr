import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data.txt')

plt.plot(data['0'])
plt.show()
