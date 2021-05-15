from logging import exception
import requests
import bz2
import os
import subprocess
import pymongo
from datetime import datetime
import sys
import shutil


class Match():

    def __init__(self, id):
        self.id = id
        self.url = ''
        self.matchend = ''
        self.teamfights = ''
        self.status = 0

    def fetch_match(self):
        '''
        Fetch the match from the dota 2 server.
        '''
        try:
            r = requests.get(self.url)
            print("Match downloaded")
            decompressed = bz2.decompress(r.content)
            print('decompressing ...')
            open('./app/temp/' + self.id + '.dem', 'wb').write(decompressed)
            print('saving as '+self.id+'.dem')
        except exception:
            self.status = 'no_download'

    def get_match_file_url(self):
        ''' fetch the full url from opendota for the match file, somehow opendota has it, idk how
        '''
        print('getting match URL')
        odotapage = requests.get(
            "https://api.opendota.com/api/matches/{} ".format(self.id))
        replay_url = odotapage.json()['replay_url']
        print('URL received: ', replay_url)
        self.url = replay_url

    def parse_match(self):

        out_combat = os.path.join(os.path.dirname(
            __file__), "games", self.id+"_combat.txt")
        # out_info = os.path.join(os.path.dirname(__file__),
        #                        "games", matchid+"_info.txt")
        # out_lifestate = os.path.join(os.path.dirname(
        #   __file__), "games", matchid + "_lifestate.txt")
        out_matchend = os.path.join(os.path.dirname(
            __file__), "games", self.id+"_matchend.txt")

        base = 'java -jar {} > {}'
        gamedir = __file__+'/'
        parsers = ['combatlog.one-jar.jar',
                   # 'info.one-jar.jar',
                   # 'lifestate.one-jar.jar',
                   'matchend.one-jar.jar']
        parsers = ['mac_claritys/'+parser for parser in parsers]
        outputs = [out_combat, out_matchend]
        # for parser, out in zip(parsers, outputs):
        # print(base.format(parser,out).split())
        s = subprocess.check_output("java -jar " +
                                    'app/mac_claritys/matchend.one-jar.jar' + " app/temp/"+self.id+'.dem',
                                    shell=True).decode(sys.stdout.encoding)
        # print(s)
        self.matchend_raw = s
        os.remove("app/temp/{}.dem".format(self.id))

    def matchend_jsonify(self):
        """
        game_id(int): the number of the game. 
        find the game record, and conver it to a json format from txt.
        """
        # print(s)
        s = self.matchend_raw.replace('│', "--SEPERATOR--")
        text = s.split('\n')
        # print(text)
        # print(len(text))
        result = []
        for n in range(0, 10):
            remdash = text[(2*n) + 3].split('--SEPERATOR--')
            result.append([remdash[1].replace(' ', ''),
                           remdash[2].replace(' ', ''),
                           remdash[3].replace(' ', ''),
                           remdash[4].replace(' ', ''),
                           remdash[5].replace(' ', ''),
                           remdash[6].replace(' ', ''),
                           remdash[7].replace(' ', ''),
                           remdash[8].replace(' ', '')])
        self.matchend = result

    # ['name': remdash[1],
    #  'level': remdash[3],
    #  'K': remdash[5],
    #  'D': remdash[7],
    #  'A': remdash[9],
    #  'Gold': remdash[11],
    #  'LH': remdash[13],
    #  'Denies': remdash[15]]

    def match_in_db(self):
        mongo_uri = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(mongo_uri)
        db = client.dota_teamfight_app
        table = db.matches
        r = table.find_one({"game_id": self.id})
        print(r)
        if r == None:
            return False
        else:
            return True

    def insert_in_db(self):
        mongo_uri = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(mongo_uri)
        db = client.dota_teamfight_app
        table = db.matches
        table.insert_one({
            "game_id": self.id,
            "matchend": self.matchend,
            "entry_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

        return True

    def retreive_matchend(self):
        mongo_uri = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(mongo_uri)
        db = client.dota_teamfight_app
        table = db.matches
        print('-' * 50)
        print('SEARCHING FOR GAME -- ', self.id)
        r = table.find_one({"game_id": self.id})
        print(r)
        self.matchend = r['matchend']
