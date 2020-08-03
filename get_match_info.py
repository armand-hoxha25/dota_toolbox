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

    df=pd.DataFrame({'hero_name':hero_name,
                    'player_name':player_name,
                    'steamid':steamid,
                    'game_team':game_team})

    return df
    
if __name__=="__main__":
    infile="./test_files/5528683650_info.txt"
    print("Running on test script, Printing final output dataframe")
    df=parse_matchinfo(infile)
    print(df.head())