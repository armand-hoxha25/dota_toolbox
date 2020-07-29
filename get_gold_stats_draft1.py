'''
get the stats on gold and experience from the combat log for each player

'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from get_match_info import parse_matchinfo
import datetime as dt
combatfile="./test_files/5528683650_combat.txt"
infofile="./test_files/5528683650_info.txt"
f=open(combatfile,'r')

txt=f.readlines()
f.close()
matchinfo=parse_matchinfo(infofile)
heroes_dict={}


def str_time_to_sec(s):
    """Convert the string time "HH:MM:SS.xxx" into total seconds.

    Args:
        s (str): string in the format mentioned above.

    Returns:
        float: floating point number of the total number of seconds.
    """    
    sec=float(s[6:])
    min_to_sec=60*float(s[3:5])
    hr_to_sec=3600*float(s[:2])
    
    return sec+min_to_sec+hr_to_sec


matchstart=None
for hero in matchinfo['hero_name']:
    m=1
    
    timestamp_gold=[]
    heroes=[]
    gold_change=[]
    experience_change=[]
    timestamp_xp=[] 
    
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
            timestamp_gold.append(str_time_to_sec(l[1:13]))
            
        
        if (hero in l) and ('XP' in l):
            s=l.find('gains')
            s=s+len('gains')
            e=l.find('XP')
            experience_change.append(int(l[s:e]))
            timestamp_xp.append(str_time_to_sec(l[1:13]))    

        if l[0]=='[':
            if matchstart==None:
                matchstart=str_time_to_sec(l[1:13])
            else:
                match_length=str_time_to_sec(l[1:13])

    timestamp_gold=timestamp_gold+ np.linspace(matchstart,match_length,num=int(match_length-matchstart)).tolist()
    gold_change=gold_change+np.ones((1,int(match_length-matchstart))).tolist()[0]
    heroes_dict[hero]={
    'timestamp_gold':timestamp_gold,
    'gold_change':gold_change,
    'experience_change':experience_change,
    'timestamp_xp':timestamp_xp
    }

df=pd.DataFrame({'gold_change':heroes_dict['npc_dota_hero_mirana']['gold_change'],\
                 'timestamp':heroes_dict['npc_dota_hero_mirana']['timestamp_gold']})

df=df.sort_values(by='timestamp')
df.plot(x='timestamp',y='gold_change')
plt.show()
