# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 23:56:59 2020

@author: Mike
"""
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
        checker = 0
        allText = i.split(' ')
        timeStamp = allText[0]
        ability = allText[4]
        hero = allText[1]
        level = allText[6].replace(')','')
        if 'illusion' in allText[-1]:
            targetHero = allText[-2] + '_illusion'
        else:
            targetHero = allText[8].replace('\n','')
                
                
        for ind,i2 in enumerate(castDict):
            if i2['Hero'] == hero:
                checker = 1
                castDict[ind]['Casts'].append({'Ability':ability,'Target':targetHero,'Level':level,'TimeStamp':timeStamp})
        if checker == 0:
            castDict.append({'Hero':hero, 'Casts':[{'Ability':ability,'Target':targetHero,'Level':level,'TimeStamp':timeStamp}]})
                    

return castDict