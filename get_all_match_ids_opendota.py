import requests
import pickle
import sys 
import pandas as pd
account_id=78812268 #32 bit steam id
api_req='''https://api.opendota.com/api/players/{}/matches?limit=6000&project=heroes'''
r=requests.get(api_req.format(account_id))
matchhistory=r.json()

pickle.dump(matchhistory,open('mike_matches.p','wb'))



## parse open dota data
match_ids=[]
heroes=[]
match_length=[]
win=[]
team_radiant=[] # player_slot < 128 is radiant
l=len(matchhistory)
n=0
for match in matchhistory:
    match_ids.append(match['match_id'])
    playersheroes=list(match['heroes'].values())
    for d in playersheroes:
        try:
            if d['account_id']==account_id:
                break
        except KeyError:
            pass
    heroes.append(d['hero_id'])
    match_length.append(match['duration'])
    win.append(True if match['radiant_win'] and match['player_slot']<128 else False)
    team_radiant.append(True if match['player_slot']<128 else False)
    n+=1
    x=str(n)+'/'+str(l)
    print(f'\r', end="")
    print(f'{x}', end="")
print(f'\n')

player_df=pd.DataFrame({'match_ids':match_ids,
'heroes':heroes,
'match_length':match_length,
'win':win,
'team_radiant':team_radiant})

