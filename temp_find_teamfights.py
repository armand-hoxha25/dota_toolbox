import pandas as pd
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt


def distance(p1, p2):
    """
    Compute Euclidean distance between units

    p1: tuple of (x1,y1) (float) : location of 1st unit
    p2: tuple of (x2,y2) (float) : location of 2nd unit
    return Distance (float) in units
    """
    return np.sqrt(((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2))


def centroid(pairs):
    """
    Compute centroid of array x and y
    pairs: list of (x,y) pairs, each pair is a tuple

    return (x,y) (tuple of floats) : centroid
    """
    return (np.mean([p[0] for p in pairs]), np.mean([p[1] for p in pairs]))


def are3close(p1, p2, p3, distThresh):
    d12 = distance(p1, p2)
    d13 = distance(p1, p3)
    d23 = distance(p2, p3)
    return (d12 < distThresh) & (d13 < distThresh) & (d23 < distThresh)


df = pd.read_csv('propertychanges.txt', sep='\t',
                 header=None, skipfooter=1, engine='python')

df.columns = ['Time_s', 'Unit', 'x', 'y']

# convertin to
df['y'] = 20000*df['y']/256
df['x'] = 20000*df['x']/256

distThresh = 1000

radiant = ['Windrunner', 'Leshrac', 'KeeperOfTheLight', 'Sven', 'Centaur']
dire = ['Obsidian_Destroyer', 'WitchDoctor',
        'PhantomLancer', 'Pudge', 'Abaddon']
radiant = list(map(lambda x: 'CDOTA_Unit_Hero_'+x, radiant))
dire = list(map(lambda x: 'CDOTA_Unit_Hero_'+x, dire))

df['team'] = df['Unit'].apply(lambda x: 0 if x in radiant else 1)
df = df.pivot(columns=['Unit', 'team'], values=['x', 'y', 'Time_s'])
t = df.iloc[:, 20:]
t = t.backfill(axis=1).ffill(axis=1).iloc[:, 0]
df = df.iloc[:, 0:19]
df['t'] = t
df = df.backfill()
df = df.drop_duplicates(subset=('t', '', ''))
df = df.dropna()
# in theory if at least 3 players of each team are close, its a teamfight
# so if nallies>=3, nenemies>=3 and allies are close with enemies = teamfight

# we go in n seconds intervals
tp = []
radcoords = []
direcoords = []
teamfight = []

window = 4
overlap = 1
time = df[('t', '', '')].tolist()

for t in time:
    tmpdf = df[df['t'] == t]
    rpairs = []
    for r in radiant:

        for c in tmpdf.columns:
            if r == c[1]:
                if c[0] == 'x':
                    indx = tmpdf[('x', r, 0)].values[0]
                elif c[0] == 'y':
                    indy = tmpdf[('y', r, 0)].values[0]
        rpairs.append((indx, indy))

    dpairs = []
    for d in dire:

        for c in tmpdf.columns:
            if d == c[1]:
                if c[0] == 'x':
                    indx = tmpdf[('x', d, 1)].values[0]
                elif c[0] == 'y':
                    indy = tmpdf[('y', d, 1)].values[0]
        dpairs.append((indx, indy))

    combs = list(combinations([0, 1, 2, 3, 4], 3))
    radcomb = None
    direcomb = None
    for c in combs:
        if are3close(rpairs[c[0]], rpairs[c[1]], rpairs[c[2]], 3000):
            radcomb = c

    for c in combs:
        if are3close(dpairs[c[0]], dpairs[c[1]], dpairs[c[2]], 3000):
            direcomb = c

    # check if we have at least 3 radiants close, and 3 dires close
    if (radcomb == None) | (direcomb == None):
        continue

    # calculate the centroid of close teammates
    rpairs = np.array(rpairs)
    rclose = rpairs[[x for x in radcomb]]
    dpairs = np.array(dpairs)
    dclose = dpairs[[x for x in direcomb]]
    rcentroid = centroid(rclose)
    dcentroid = centroid(dclose)

    if distance(rcentroid, dcentroid) > 3000:
        print("radiant: {} , dire: {}".format(rcentroid, dcentroid))
        print('teams too far appart')
        continue

    print('-'*30)
    tp.append(t)
    teamfight.append(centroid([rcentroid, dcentroid]))
    radcoords.append(rpairs)
    direcoords.append(dpairs)

f, ax = plt.subplots()

markers = ['o', '^', '+', 's']
for t, r, d, m in zip(teamfight, radcoords, direcoords, markers):
    rx = []
    ry = []
    dx = []
    dy = []
    ax.add_patch(plt.Circle(t, 1000, color='b', fill=False))
    for rc in r:
        rx.append(rc[0])
        ry.append(rc[1])
    for dc in d:
        dx.append(dc[0])
        dy.append(dc[1])

    ax.scatter(dx, dy, c=[1, 0, 0], marker=m)
    ax.scatter(rx, ry, c=[0, 1, 0], marker=m)

ax.set_xlim((0, 20000))
ax.set_ylim((0, 20000))

f.savefig('teamfights.png')
