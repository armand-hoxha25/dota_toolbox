import requests
import bz2
import subprocess
import os
import pandas as pd

'''The match object, the mother of them all!!!'''

class Match:
    def __init__(self,matchid):
        self.matchid=matchid
        self.TotalGoldEarned=dict()
        self.LastHits=None
        self.Players=None
        self.replay_url=None
        self.odotadict=None
        self.parsed_info=None
        self.parsed_lifestate=None
        self.combat=None
        self.matchend=None
        self.matchinfo=None

        self.fetch_match()
        self.parse_match()
        self.parse_matchinfo()
    

    def fetch_match(self):
        '''
        Fetch the match from the dota 2 server.
        '''
        print("Fetching match id :", self.matchid)
        self.get_match_file_url()
        r=requests.get(self.replay_url)
        decompressed=bz2.decompress(r.content)
        open('temp_replay.dem','wb').write(decompressed)
        print("Match downloaded")
        pass

    def parse_match(self):
        '''
        parse the data from the match
        populate the match details 
        '''
        test_file=os.path.join(os.path.dirname(__file__),"temp_replay.dem")

        # parse the match .dem file into a txt files
        out_combat=os.path.join(os.path.dirname(__file__),"test_files","temp_combat.txt")
        out_info=os.path.join(os.path.dirname(__file__),"test_files","temp_info.txt")
        out_lifestate=os.path.join(os.path.dirname(__file__),"test_files","temp_lifestate.txt")
        out_matchend=os.path.join(os.path.dirname(__file__),"test_files","temp_matchend.txt")

        base='java -jar {} > {}'

        parsers=['combatlog.one-jar.jar',
             'info.one-jar.jar',
             'lifestate.one-jar.jar',
             'matchend.one-jar.jar']
        parsers=['/clarity_jars/'+parser for parser in parsers]
        outputs=[out_combat, out_info, out_lifestate, out_matchend]
        for parser,out in zip(parsers,outputs):
            #print(base.format(parser,out).split())
            exec_call="java -jar "+os.path.dirname(__file__)+\
                parser + " "+test_file + " > " +out 
            print(exec_call)
            s = subprocess.call(exec_call,
                shell = True, stderr=subprocess.STDOUT) 
            if s==0:
                pass
            else:
                print("Could not parse data")
            print(", return code", s)   

        pass

    def get_match_file_url(self):
        ''' fetch the full url from opendota for the match file, somehow opendota has it, idk how
        '''        
        odotapage=requests.get("https://api.opendota.com/api/matches/{} ".format(self.matchid))
        self.replay_url = odotapage.json()['replay_url']

        pass

    def parse_matchfile(self):
        self.parse_matchinfo()

        pass

    def parse_matchinfo(self):
        """Parses the match info from the Clarity info.one-jar.jar output.
        Includes the players hero name, player name, steamd id and
        game team. 

        Args:
            infile (str): local path to the file

        Returns:
            df(pandas.DataFrame): Pandas dataframe with hero_name,player_name,steamid,game_team
            as columns.
        """    
        f=open(os.path.join(os.path.dirname(__file__),"test_files","temp_info.txt"),'r')
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

        hero_names=[h.replace('npc_dota_hero_','') for h in hero_name]
        df=pd.DataFrame({'hero_name':hero_names,
                        'player_name':player_name,
                        'steamid':steamid,
                        'game_team':game_team})

        self.matchinfo=df
        pass

    def get_TotalGoldEarned(self):

        timestamp_d=[]
        timestamp_r=[]

        with open("test_files/temp_combat.txt") as f:
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
                    timestamp_r.append(self.str_time_to_sec(last_timestamp))
            
            elif l[0:4]==" Dir":
                myline=l.split(',')[1:]
                if myline !=[]:
                    dire_lines.append(myline)
                    timestamp_d.append(self.str_time_to_sec(last_timestamp))

        heroes=self.matchinfo['hero_name'].tolist()

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

        self.TotalGoldEarned['Radiant']=pd.DataFrame(Dr)
        self.TotalGoldEarned['Dire']=pd.DataFrame(Dd)

        pass
        
    
    def str_time_to_sec(self, s):
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