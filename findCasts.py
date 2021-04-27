# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 23:56:59 2020

@author: Mike
"""

import pandas as pd


def getCasts():

    combatLog = r'C:\\Users\\Mike\\Documents\\GitHub\\dota_toolbox\\test_files\\5538111463_1967011834_combat.txt'
    with open(combatLog,"r") as f:
        
        g = list(f)
        
        indexList = []
        
        for ind, text in enumerate(g):
            if 'cast' in text:
                indexList.append(ind)
        
        castDict = []
        
        
        for i3 in indexList:
            i = g[i3]
            
            allText = i.split(' ')
            timeStamp = allText[0]
            ability = allText[4]
            hero = allText[1]
            level = allText[6].replace(')','')
            
            if 'illusion' in allText[-1]:
                targetHero = allText[-2] + '_illusion'
            else:
                targetHero = allText[8].replace('\n','')
            
            
            
            castDict.append({"Caster":[hero],"Ability":[ability],"Target":[targetHero],"Level":[level],"TimeStamp":[timeStamp]})
                    
            # for ind,i2 in enumerate(castDict):
            #     if i2['Hero'] == hero:
            #         checker = 1
            #         castDict[ind]['Casts'].append({'Ability':ability,'Target':targetHero,'Level':level,'TimeStamp':timeStamp})
            # if checker == 0:
            #     castDict.append({'Hero':hero, 'Casts':[{'Ability':ability,'Target':targetHero,'Level':level,'TimeStamp':timeStamp}]})
        castDict = pd.DataFrame(castDict)              
    
    return castDict


def getDamage():

    combatLog = r'C:\\Users\\Mike\\Documents\\GitHub\\dota_toolbox\\test_files\\5538111463_1967011834_combat.txt'
    with open(combatLog,"r") as f:
        
        g = list(f)
        
        indexList = []
        
        for ind, text in enumerate(g):
            if 'hits' in text and 'illusion' in text:
                indexList.append(ind)
        
        hitDict = []
        
        
        for i3 in indexList:
            i = g[i3]
            
            allText = i.split(' ')
            timeStamp = allText[0]
            
            if 'illusion' in allText[2]:
                hero = allText[1]+'_illusion'
                if 'illusion' in allText[5]:
                    targetHero = allText[4]+'_illusion'
                    damageSource = allText[7]
                    damageDone = allText[9]
                    healthChange = allText[-1][1:-2]
                targetHero = allText[4]
                damageSource = allText[6]
                damageDone = allText[8]
                healthChange = allText[-1][1:-2]
            if 'illusion' in allText[4]:
                hero = allText[1]
                targetHero = allText[3]+'_illusion'
                damageSource = allText[6]
                damageDone = allText[8]
                healthChange = allText[-1][1:-2]
            hero = allText[1]
            targetHero = allText[3]
            damageSource = allText[5]
            damageDone = allText[7]
            healthChange = allText[-1][1:-2]
            
                
            
            
            
            castDict.append({"Caster":[hero],"Ability":[ability],"Target":[targetHero],"Level":[level],"TimeStamp":[timeStamp]})
                    
            # for ind,i2 in enumerate(castDict):
            #     if i2['Hero'] == hero:
            #         checker = 1
            #         castDict[ind]['Casts'].append({'Ability':ability,'Target':targetHero,'Level':level,'TimeStamp':timeStamp})
            # if checker == 0:
            #     castDict.append({'Hero':hero, 'Casts':[{'Ability':ability,'Target':targetHero,'Level':level,'TimeStamp':timeStamp}]})
        castDict = pd.DataFrame(castDict)              
    
    return castDict

gg = getCasts()