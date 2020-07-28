'''
get the stats on gold and experience from the combat log for each player

'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from get_match_info import parse_matchinfo

combatfile="./test_files/5528683650_combat.txt"
infofile="./test_files/5528683650_info.txt"
f=open(combatfile,'r')

txt=f.readlines()
f.close()
matchinfo=parse_matchinfo(infofile)
timestamps=[]
heroes=[]
gold_change=[]
experience_change=[]
hero=matchinfo['hero_name'][0]
m=1
for l in txt:
    # find the gold change, and append it
    if (hero in l) and ('gold' in l):
        s=l.find('looses')
        if s==-1:
            s=l.find('receives')
            s=s+len('receives')
            m=1
        else:
            s=s+len('looses')
            m=-1
        e=l.find('gold')
        gold_change.append(m*int(l[s:e]))
        
    
    if (hero in l) and ('XP' in l):
        s=l.find('gains')
        s=s+len('gains')
        e=l.find('XP')
        experience_change.append(int(l[s:e]))
        


