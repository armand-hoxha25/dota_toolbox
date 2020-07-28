import pandas as pd

infile="./test_files/5528683650_info.txt"
f=open(infile,'r')


txt=f.readlines()
f.close()
hero_name=[]
player_name=[]
steamid=[]
game_team=[]
infotags=[]
for i,l in enumerate(txt):
    if "player_info" in l:
        infotags.append(i)

for i in infotags:
    hero_name.append(txt[i+1].replace("hero_name:","").split('''"''')[1])
    player_name.append(txt[i+2].replace("player_name:","").split('''"''')[1])
    steamid.append(int(txt[i+4].replace("steamid:","")))
    game_team.append(int(txt[i+5].replace("game_team:","")))

df=pd.DataFrame({'hero_name':hero_name,
                 'player_name':player_name,
                 'steamid':steamid,
                 'game_team':game_team})

df.to_csv("temp_match_info.csv")
    
        