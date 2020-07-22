import requests
import datetime
import time
import shutil
import pandas as pd
import seaborn as sns
steamId = '76561198089787694'
numMatches = '100'
dotaId = 129521966

baseApi = 'https://api.opendota.com/api/'

def getHeroList():
    apiCall = baseApi + 'constants/hero_names'
    apiReturn = requests.get(apiCall)
    apiReturn = apiReturn.json()
    names = []
    ids = []
    for d in range(0,len(apiReturn.keys())):
         fullName = list(apiReturn.keys())[d]
         heroSpecs = apiReturn[fullName]
        
         names.append(heroSpecs['localized_name'])
         ids.append(heroSpecs['id'])
         
    heroList = pd.DataFrame({'Hero_IDs':ids,'Hero_Names':names})
    return heroList