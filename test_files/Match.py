import requests
import bz2
'''The match object, the mother of them all!!!'''

class Match:
    def __init__(self,matchid):
        self.matchid=matchid
        self.TotalGoldEarned=None
        self.LastHits=None
        self.Players=None
    

    def fetch_match(self,matchid):
        '''
        Fetch the match from the dota 2 server.
        '''
        print("Fetching match id :", matchid)
        r=requests.get("http://replay123.valve.net/570/5561002371_634942479.dem.bz2")
        pass

    def parse_match(self,match_file):
        '''
        parse the data from the match
        populate the match details 
        '''
        pass

    def get_match_file_url(self):
        ''' fetch the full url from opendota for the match file, somehow opendota has it, idk how
        '''
        pass