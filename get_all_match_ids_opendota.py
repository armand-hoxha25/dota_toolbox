import requests
import pickle

api_req='''https://api.opendota.com/api/players/78812268/matches'''
r=requests.get(api_req)
matchhistory=r.json()

pickle.dump(j,open('armand_matches.p','wb'))
