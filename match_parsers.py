import pandas as pd

def parse_matchinfo(infile):
    """Parses the match info from the Clarity info.one-jar.jar output.
       Includes the players hero name, player name, steamd id and
       game team. 

    Args:
        infile (str): local path to the file

    Returns:
        df(pandas.DataFrame): Pandas dataframe with hero_name,player_name,steamid,game_team
        as columns.
    """    
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

    hero_name=[x[14:] for x in hero_name]
    df=pd.DataFrame({'hero_name':hero_name,
                    'player_name':player_name,
                    'steamid':steamid,
                    'game_team':game_team})

    return df
    

def str_time_to_sec(s):
    """Convert the string time "HH:MM:SS.xxx" into total seconds.

    Args:
        s (str): string in the format mentioned above.

    Returns:
        float: floating point number of the total number of seconds.
    """    
    
    sec=float(s[7:12])
    min_to_sec=60*float(s[4:6])
    hr_to_sec=3600*float(s[1:3])
    
    return sec+min_to_sec+hr_to_sec   

def parse_networth(f,matchinfo):
    timestamp_d=[]
    timestamp_r=[]

    with open(f) as f:
        txt=f.readlines()
    dire_lines=[]
    radiant_lines=[]
    last_timestamp='[00:00:00.000]'
    for l in txt:
        if l[0]=='[':
            last_timestamp=l
        
        if l[0:4]==" Rad" or l[0:4]=="Radi":
            myline=l.split(',')[1:]
            if myline != []:
                radiant_lines.append(myline)
                timestamp_r.append(str_time_to_sec(last_timestamp))
        
        elif l[0:4]==" Dir":
            myline=l.split(',')[1:]
            if myline !=[]:
                dire_lines.append(myline)
                timestamp_d.append(str_time_to_sec(last_timestamp))

    heroes=matchinfo['hero_name']

    #first 5 are radiant, latter 5 are the dire heroes
    Dr=dict()
    Dd=dict()
    if [] in radiant_lines:
        radiant_lines.remove([])
    if [] in dire_lines:
        dire_lines.remove([])

    for h in range(0,5):
        hero_data=[]
        for r in radiant_lines:
            hero_data.append(int(r[h]))
        Dr[heroes[h]]= hero_data

    for h in range(5,10):
        hero_data=[]
        for r in dire_lines:
            hero_data.append(int(r[h-5]))
        Dd[heroes[h]]= hero_data
    Dd['timestamp']=timestamp_d
    Dr['timestamp']=timestamp_r

    Radiant=pd.DataFrame(Dr)
    Dire=pd.DataFrame(Dd)

    return Radiant,Dire

if __name__=="__main__":
    matchinfo_file="./test_files/temp_info.txt"
    print("Running on test script, Printing final output dataframe")
    matchinfo=parse_matchinfo(matchinfo_file)
    print(matchinfo.head())

    combat_file="./test_files/temp_combat.txt"
    Radiant,Dire=parse_networth(combat_file,matchinfo)