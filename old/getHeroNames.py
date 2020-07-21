# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import shutil
import pandas as pd
import seaborn as sns

apiKey = 'C0653C275405A0DC18DDCE46BA8645C2'
steamId = '76561198089787694'
numMatches = '100'
dotaId = 129521966

  
#Get Hero List




def getHeroList(apiKey):
    """Returns a list of Hero Names and their corresponding Hero IDs"""
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
        
    return [names,ids]

# Call x matches by steam id
    
def getMatchHeroNames(matchPlayerDetails,heroList,idList):
    """Takes player dictionary from a match and returns each hero played
    ['result']['matches'][0]['players']"""
    
    matchPlayerDetails = matchPlayerDetails['players']
    heroesPlayed = []
    for d in range(0,len(matchPlayerDetails)):
        
        heroIdPlayed = matchPlayerDetails[d]['hero_id']
        heroesPlayed.append(heroList[idList.index(heroIdPlayed)])
    return heroesPlayed
    
def getMatchPlayerIds(matchPlayerDetails):
    """Takes p`layer dictionary from a match and returns each player's steam ID"""
    playerIds = []
    matchPlayerDetailsUnpack = matchPlayerDetails['players']
    for d in matchPlayerDetailsUnpack:
        if 'account_id' in d.keys():
            steamId = d['account_id']
            playerIds.append(steamId)
            
    return(playerIds)
        
    
    
def getPlayerMatchHistory(steamId,numMatches,apiKey):
    """Makes an api call for given steamId's last x matches, up to 100 matches"""
    apiCallStringBase = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?matches_requested={}_?&account_id={}_?&key={}'
    # steamId = '76561198089787694'
    # numMatches = '100'
    # apiKey = 'C0653C275405A0DC18DDCE46BA8645C2';
    # apiCall = apiCallStringBase.format(numMatches,steamId,apiKey)
    # apiReturn = requests.get(apiCall)
    if int(numMatches) <= 100:
        apiCall = apiCallStringBase.format(numMatches,steamId,apiKey)
        apiReturn = requests.get(apiCall)
        matchDict = apiReturn.json()['result']['matches']
        return matchDict
    
    
def countHeroesPlayed(dotaId, matchHistory, heroList, idList):
    """Go through a players match history and get a list/count of all heroes played and plot"""
    
    
    heroesPlayedDict = {}
    
    for t in range(0,len(matchHistory)):
        
        
        tempMatchDeets = matchHistory[t]
        playerIds = getMatchPlayerIds(tempMatchDeets)
        heroesPlayed = getMatchHeroNames(tempMatchDeets,heroList,idList)
        playerIndex = playerIds.index(dotaId)
        heroPlayed = heroesPlayed[playerIndex]
        
        
        if len(heroesPlayedDict) == 0:
            heroesPlayedDict[0] = {'Hero': heroPlayed,'TimesPlayed': 1}
        else:
            checker = 0
            for i in range(0,len(heroesPlayedDict)):
                if heroesPlayedDict[i]['Hero'] == heroPlayed:
                    heroesPlayedDict[i]['TimesPlayed'] = heroesPlayedDict[i]['TimesPlayed'] + 1
                    checker = 1
                    
            if checker == 0:
                heroesPlayedDict[len(heroesPlayedDict)] = {'Hero': heroPlayed,'TimesPlayed': 1}
            
    return heroesPlayedDict

def downloadHeroPortraits(names):
    
    apiBase = 'http://cdn.dota2.com/apps/dota2/images/heroes/{}_{}'
    for n in range(0,len(names)):
        apiCall = apiBase.format(names[n],'vert.jpg')
    
        apiReturn = requests.get(apiCall,stream = True)
        
        apiReturn.raw.decode_content = True
        
        filename = apiCall.split('/')[-1]
        
        with open(filename,'wb') as f:
            shutil.copyfileobj(apiReturn.raw, f)
            
def plotHeroesPlayed(heroesPlayedList):
    
    heroesPlayedNames = []
    heroesPlayedCounts = []
    for i in range(0,len(heroesPlayedList)):
        heroesPlayedNames.append(heroesPlayedList[i]['Hero'])
        heroesPlayedCounts.append(heroesPlayedList[i]['TimesPlayed'])
    
    heroStats = {'heroNames': heroesPlayedNames, 'playCount': heroesPlayedCounts}
    
    h = sns.barplot(data=heroStats,x='heroNames',y='playCount')
    
    h.set_xticklabels(h.get_xticklabels(),rotation=45)
    
    h.set(xlabel = 'Hero', ylabel = 'Times Played', title = 'Hero History')
    
        
    
   
    


            
                        
                    
        
        
        
        
            
        




    
    