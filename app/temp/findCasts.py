# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 23:56:59 2020

@author: Mike
"""

import pandas as pd
import os
import re
import numpy as np
filename = '5538111463_1967011834_combat.txt'
print(__file__)
filedir = os.path.dirname(__file__)
print(filedir)
test_file = os.path.join(filedir, filename)


def timestamp_to_s(timestamp):
    return(
        int(timestamp[1:3])*3600 +
        int(timestamp[4:6])*60 +
        int(timestamp[7:9])
    )


def getCasts(test_file):

    combatLog = test_file
    with open(combatLog, "r") as f:

        g = list(f)

        indexList = []

        for ind, text in enumerate(g):
            if "cast" in text:
                indexList.append(ind)

        castDict = []

        for i3 in indexList:
            i = g[i3]

            allText = i.split(" ")
            timeStamp = allText[0]
            ability = allText[4]
            hero = allText[1]
            level = allText[6].replace(")", "")

            if "illusion" in allText[-1]:
                targetHero = allText[-2] + "_illusion"
            else:
                targetHero = allText[8].replace("\n", "")

            castDict.append(
                {
                    "Caster": [hero],
                    "Ability": [ability],
                    "Target": [targetHero],
                    "Level": [level],
                    "TimeStamp": [timeStamp],
                }
            )
        castDict = pd.DataFrame(castDict)

    return castDict


def getDamage(test_file):

    combatLog = test_file
    with open(combatLog, "r") as f:

        g = list(f)

        indexList = []

        for ind, text in enumerate(g):
            if "hits" in text and "for" in text:
                indexList.append(ind)

        hitDict = []

        for i3 in indexList:
            i = g[i3]

            allText = i.split(" ")
            timeStamp = allText[0]
            timeStamp = timestamp_to_s(timeStamp)
            if "illusion" in allText[2]:
                hero = allText[1] + "_illusion"
            else:
                hero = allText[1]
            for ind, text in enumerate(allText):
                if "hits" in text:
                    if "illusion" in allText[ind + 2]:
                        targetHero = allText[ind + 1] + "_illusion"
                    else:
                        targetHero = allText[ind + 1]
                if "with" in text:
                    damageSource = allText[ind + 1]
                if "for" in text:
                    damageDone = allText[ind + 1]

            if 'damage' in allText[-1]:
                startingHealth = int(damageDone)
                endHealth = 0
            else:
                healthChange = allText[-1][1:-2]

                healthChange = healthChange.split('->')
                startingHealth = int(healthChange[0])
                endHealth = int(healthChange[1])

            #hero = hero.replace('npc_dota_hero_', '')

            hitDict.append(
                {

                    "FromHero": hero,
                    "DamageSource": damageSource,
                    "Target": targetHero,
                    "DamageDone": int(damageDone),
                    "TimeStamp": timeStamp,
                    "HealthBefore": startingHealth,
                    "HealthAfter": endHealth
                }
            )

        hitDict = pd.DataFrame(hitDict)

    return hitDict


def splitDamageDf(hitTable):
    lastTime = hitTable.iloc[0]['TimeStamp']
    tfList = []
    iter = 0
    
    for tableInd, i in enumerate(hitTable.iloc):

        if i['TimeStamp']-lastTime > 25:

            lastTime = lastTime + 25
            if len(tfList)<1:
                tempTable = hitTable.iloc[iter:tableInd+1]
                tfList.append(tempTable)
                iter = tableInd
            else:
                overlapInd = iter + round(((tableInd-iter)/2))
                tempTable = hitTable.iloc[overlapInd:tableInd+1]
                tfList.append(tempTable)
                iter = tableInd
                

    return tfList


def filter_out_non_hero_dmg(damage_df):

    heroStr = 'npc_dota_hero'
    indsKeep = []
    for i in range(0, damage_df.shape[0]):
        if (heroStr in damage_df['FromHero'][i]) and (heroStr in damage_df['Target'][i]) and (not ('illusion' in damage_df['FromHero'][i])) and (not ('illusion' in damage_df['Target'][i])) and (not(damage_df['FromHero'][i] in damage_df['Target'][i])):
                        indsKeep.append(i)

    return damage_df.iloc[indsKeep]


def average_damage(data, window=5, overlap=1):
    timewindows = np.linspace(data['TimeStamp'].tolist()[0],
                              data['TimeStamp'].tolist()[-1],
                              int(np.round((data['TimeStamp'].tolist()[-1]
                                            - data['TimeStamp'].tolist()[0])/window)))
    if (len(timewindows) % 2):
        timewindows = np.delete(timewindows, len(timewindows)-1)
    timewindows = np.reshape(timewindows, (int(timewindows.shape[0]/2), 2))
    timepoint = np.mean(timewindows, axis=1)
    damagewindow = []
    for i, tp in enumerate(timepoint):
        ts = timewindows[i, 0]
        te = timewindows[i, 1]
        damagewindow.append(data[(data['TimeStamp'] > ts) &
                                 (data['TimeStamp'] < te)]
                            ['DamageDone'].sum())

    return timepoint, damagewindow

def findTeamfights(filteredDmgDF):
  
    teamfightList = []
    
    teamfightActive = 0
    teamfightDamageList = []
    for i in range(0,len(filteredDmgDF)):
        
        tempDf = filteredDmgDF[i]
        if teamfightActive > 0 and teamfightActive < 3:
            teamfightActive = teamfightActive + 1
        elif teamfightActive == 3 or teamfightActive == 0:
            teamfightActive = 0
            
            if len(tempDf)<1:
                continue
            elif len(teamfightDamageList)>30:
                
                
                
                fromHeros = tempDf.FromHero.unique()
                toHeros = tempDf.Target.unique()
                teamfightSTD = np.std(teamfightDamageList)
                teamfightMean = np.mean(teamfightDamageList)
                currentSum = tempDf.DamageDone.sum()
                if (len(fromHeros)>3) and (len(toHeros)>3) and (currentSum>teamfightMean+teamfightSTD) and (len(tempDf[tempDf['HealthAfter']==0])>0):
                    dfsToMerge = filteredDmgDF[i-1:i+2]
                    teamfightTemp = pd.concat(dfsToMerge)
                    
                    teamfightList.append(teamfightTemp)
                    print(i)
                    teamfightTemp = []
                    teamfightActive = 1
                    
                teamfightDamageList.pop(0)
                teamfightDamageList.append(tempDf.DamageDone.sum())            
                        
                
                            
                       
            else:
                teamfightDamageList.append(tempDf.DamageDone.sum())
                
                
    teamfightDF = pd.DataFrame()
    teamfightAll = []

    for i in teamfightList:
        fromList = []
        toList = []
        fromHeroes = i['FromHero'].unique()
        toHeroes = i['Target'].unique()
        killHeroes = i[i['HealthAfter']==0]['FromHero'].unique()
        killList = []
        
        
        for i2 in fromHeroes:
            tempDf = i[i['FromHero']==i2]
            tempDf = pd.pivot_table(tempDf,values='DamageDone',index=['FromHero','Target','DamageSource'],aggfunc=np.sum)
            fromList.append(tempDf)
            
        fromDF = pd.concat(fromList)
        
        for i2 in toHeroes:
            tempDf = i[i['Target']==i2]
            tempDf = pd.pivot_table(tempDf,values='DamageDone',index=['Target','FromHero','DamageSource'],aggfunc=np.sum)
            toList.append(tempDf)
        toDF = pd.concat(toList)
            
        for i2 in killHeroes:
            tempDf = i[i['HealthAfter']==0]
            tempDf = tempDf[tempDf['FromHero']==i2]
            heroesKilled = tempDf['Target'].unique()
            killDF = pd.DataFrame({'FromHero':[i2],'HeroesKilled':[heroesKilled]})
            killList.append(killDF)
        killDF = pd.concat(killList)
        
        
        
        bigTempDF = {'FromList':fromDF,'ToList':toDF,'KillList':killDF}
        teamfightAll.append(bigTempDF)
        
    
    
    return teamfightAll
    
                
         
                
        
        
        
        
        
        
gg = getCasts(test_file)
hh = getDamage(test_file)

filtdmg = filter_out_non_hero_dmg(hh)
tt = splitDamageDf(filtdmg)
qq = findTeamfights(tt)

