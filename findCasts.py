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
            if 'hits' in text and 'for' in text:
                indexList.append(ind)
        
        hitDict = []
        
        
        for i3 in indexList:
            i = g[i3]
            
            allText = i.split(' ')
            for ind, text in allText:
                allText[ind] = allText[ind].replace('[','')
                allText[ind] = allText[ind].replace(']','')
                
            timeStamp = allText[0][0]
            if 'illusion' in allText[2]:
                hero = allText[1]+'_illusion'
            else:
                hero = allText[1]
            for ind, text in enumerate(allText):
                if 'hits' in text:
                    if 'illusion' in allText[ind+2]:
                        targetHero = allText[ind+1]+'_illusion'
                    else:
                        targetHero = allText[ind+1]
                if 'with' in text:
                    damageSource = allText[ind+1]
                if 'for' in text:
                    damageDone = allText[ind+1]
            healthChange = allText[-1][1:-2]
                
            
            
            
            hitDict.append({"HealthChange":healthChange,"FromHero":hero,"DamageSource":damageSource,"Target":targetHero,"DamageDone":damageDone,"TimeStamp":timeStamp})
                    
           
        hitDict = pd.DataFrame(hitDict)              
    
    return hitDict

        


gg = getCasts()
hh = getDamage()




    
