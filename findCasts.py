# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 23:56:59 2020

@author: Mike
"""

import pandas as pd
import os 
import re
import numpy as np
filename='5538111463_1967011834_combat.txt'
print(__file__)
filedir=os.path.dirname(__file__)
print(filedir)
test_file=os.path.join(filedir,filename)


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

            # for ind,i2 in enumerate(castDict):
            #     if i2['Hero'] == hero:
            #         checker = 1
            #         castDict[ind]['Casts'].append({'Ability':ability,'Target':targetHero,'Level':level,'TimeStamp':timeStamp})
            # if checker == 0:
            #     castDict.append({'Hero':hero, 'Casts':[{'Ability':ability,'Target':targetHero,'Level':level,'TimeStamp':timeStamp}]})
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
           # for ind, text in allText:
            #    allText[ind] = allText[ind].replace("[", "")
            #    allText[ind] = allText[ind].replace("]", "")

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
                
            hero = hero.replace('npc_dota_hero_','')

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


def findTeamfights(hitTable):
    lastTime = hitTable.iloc[0]['TimeStamp']
    tfList = []
    iter = 0
    for tableInd,i in enumerate(hitTable.iloc):
        
        if i['TimeStamp']-lastTime>5:
            
            lastTime = lastTime + 5
            tempTable = hitTable.iloc[iter:tableInd+1]
            tfList.append(tempTable)
            iter = tableInd
    
    return tfList
        
gg = getCasts(test_file)
hh = getDamage(test_file)
tt = findTeamfights(hh)

