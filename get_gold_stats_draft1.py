'''
get the stats on gold and experience from the combat log for each player

'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

infile="./test_files/5528683650_combat.txt"
f=open(infile,'r')

txt=f.readlines()
timestamps=[]
heroes=[]
gold_change=[]
experience_change=[]
for txtline in txt:
    if 'npc_dota_hero' in txtline:
        items=txtline.split()
        for item in items:
            if ('npc_dota_hero' in item) and item[-2:]!="'s":
                heroes.append(item) 

heroes=list(set(heroes))

