import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('lifestates.txt', sep='\t',
                 header=None, skipfooter=1, engine='python')

df.columns = ['Time_s', 'Unit', 'team']

#2 is radiant
#3 is dire

# if 3 deaths happen within 30 second window, then its a teamfight?

window = 30
time_list = df['Time_s'].tolist()
nsteps = int(np.round((time_list[-1]-time_list[0])/window))
time = np.linspace(time_list[0], time_list[-1], nsteps)

n = 0
tstart = []
tend = []
ndeaths = []

while n < len(time)-1:
    tmpdf = df[(df['Time_s'] > time[n]) & (df['Time_s'] < time[n+1])]
    tstart.append(time[n])
    tend.append(time[n+1])
    ndeaths.append(tmpdf.shape[0])
    n += 1

plt.bar(x=tstart, height=ndeaths, width=15)
plt.ylabel('ndeaths')
plt.xlabel('Time in seconds')
plt.title('number of deaths in 30sec windows')
plt.show()
