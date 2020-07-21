import requests
import pickle

api_req='''https://api.opendota.com/api/players/78812268/matches?limit=6000&project=heroes'''
r=requests.get(api_req)
matchhistory=r.json()

pickle.dump(matchhistory,open('armand_matches.p','wb'))



## parse open dota data
match_ids=[]
heroes_played=[]
match_length=[]
win=[]
team_radiant=[] # player_slot < 128 is radiant
