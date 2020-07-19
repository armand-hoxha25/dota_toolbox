# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import datetime
import time
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
    api2ndcall = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?matches_requested={}_?&start_at_match_id={}_?&account_id={}_?&key={}'
    # steamId = '76561198089787694'
    # numMatches = '100'
    # apiKey = 'C0653C275405A0DC18DDCE46BA8645C2';
    # apiCall = apiCallStringBase.format(numMatches,steamId,apiKey)
    # apiReturn = requests.get(apiCall)
    if int(numMatches) <= 100:
        apiCall = apiCallStringBase.format(100,steamId,apiKey)
        apiReturn = requests.get(apiCall)
        matchDict = apiReturn.json()['result']['matches']
    else:
        apiCall = apiCallStringBase.format(100,steamId,apiKey)
        apiReturn = requests.get(apiCall)
        matchDict = apiReturn.json()['result']['matches']
        old_start_at=0
        cond=True
        while cond==True:
            start_at=str(matchDict[-1]['match_id'])
            print(start_at)
            api2ndcall_exec = api2ndcall.format(100,start_at,steamId,apiKey)
            apiReturn = requests.get(api2ndcall_exec)
            if apiReturn.ok:
                cond==True
                matchDict=matchDict+apiReturn.json()['result']['matches']
                if start_at==old_start_at:
                    cond=False
                else:
                    old_start_at=start_at
            else:
                cond=False
            print(len(matchDict))
            if len(matchDict)>numMatches:
                return_matches=matchDict[0:numMatches]
                cond=False
            time.sleep(0.1)
    return matchDict

 def unix_to_date(unix_time):
     return datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')   

 def unix_to_date(unix_time):
     return datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')   


for j in range(0,333):
    print(unix_to_date(matchDict[j]['start_time']))

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



def get_player_ids(steam64ID):
    '''
    Searches through the steamid.xyz and scrapes the name
    id: (str) steam id of the user to be searched
    
    returns name (str)
    '''
    page=requests.get("https://steamid.xyz/{}".format(steam64ID))
    txt=page.text
    template_nick='''Nick Name\r\n<input type="text" onclick="this.select();" value="'''
    template_nick_end='''">\r\nProfile URL\r\n<input type="text'''
    pad=len(template_nick)
    start=txt.find(template_nick)
    end=txt.find(template_nick_end)
    ## find the end of the name
    if start ==-1:
        return "Unknown","Unknown"
    nick_name=txt[start+pad:end]


    template_dotaid='''Steam32 ID\r\n<input type="text" onclick="this.select();" value="'''
    template_dotaid_end='''">\r\nSteam64 ID\r\n<input type="text'''
    pad=len(template_dotaid)
    start=txt.find(template_dotaid)
    end=txt.find(template_dotaid_end)
    if start ==-1:
        return "Unknown", "Unknown"
    dotaid=txt[start+pad:end]

    return nick_name,int(dotaid)
            
def get_all_matches()
    