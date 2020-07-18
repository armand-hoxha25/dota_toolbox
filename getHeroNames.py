# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests

apiKey = 'C0653C275405A0DC18DDCE46BA8645C2';
 
#Get Hero List

heroApiCall = 'http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1/?itemizedonly=true_?&key={}'

heroListOrig = requests.get(heroApiCall.format(apiKey))

heroListTemp = heroListOrig.json()['result']['heroes']
names = []
ids = []
for d in heroListTemp:
    fullName = d['name']
    delimiter = '_'
    names.append(delimiter.join(fullName.split('_')[3:]))
    ids.append(d['id'])

# Call x matches by steam id

apiCallStringBase = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?matches_requested={}_?&account_id={}_?&key={}'

steamId = '76561198089787694'

matchesToCall = '1'

r = requests.get(apiCallStringBase.format(matchesToCall,steamId,apiKey))

matchDeets = r.json()

#get heroes played in the match

playerDeets = matchDeets['result']['matches'][0]['players']

heroesPlayed = []
for d in playerDeets:
    heroIdPlayed = d['hero_id']
    heroesPlayed.append(names[ids.index(heroIdPlayed)])
    
    