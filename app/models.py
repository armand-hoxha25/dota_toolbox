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
        self.MONGODBURI = MONGO_DB_URI = MONGO_DB_URI = MONGO_DB_URI = "mongodb+srv://{}:{}@dota-toolbox-east.1gro0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"\
            .format(os.environ.get("MONGO_USER"), os.environ.get("MONGO_PASSWORD"))

    def fetch_match(self):
        '''
        Fetch the match from the dota 2 server.
        '''
        try:
            r = requests.get(self.url)
            sys.stdout.write("Match downloaded \n")
            decompressed = bz2.decompress(r.content)
            sys.stdout.write('decompressing ...')
            open('./app/temp/' + self.id + '.dem', 'wb').write(decompressed)
            sys.stdout.write('saving as {}.dem'.format(self.id))
        except exception:
            self.status = 'no_download'

    def get_match_file_url(self):
        ''' fetch the full url from opendota for the match file, somehow opendota has it, idk how
        '''
        sys.stdout.write('getting match URL \n')
        odotapage = requests.get(
            "https://api.opendota.com/api/matches/{} ".format(self.id))
        replay_url = odotapage.json()['replay_url']
        sys.stdout.write('URL received: {}'.format(replay_url))
        self.url = replay_url

    def parse_match(self):
        sys.stdout.write('parsing match \n')
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
        parsers = ['clarity_jars/'+parser for parser in parsers]
        outputs = [out_combat, out_matchend]
        # for parser, out in zip(parsers, outputs):
        # print(base.format(parser,out).split())
        s = subprocess.check_output("java -jar " +
                                    'app/clarity_jars/matchend.one-jar.jar' + " app/temp/"+self.id+'.dem',
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
        client = pymongo.MongoClient(self.MONGODBURI)
        db = client.dota_teamfight_app
        table = db.matches
        r = table.find_one({"game_id": self.id})
        sys.stdout.write(str(r))
        if r == None:
            return False
        else:
            return True

    def insert_in_db(self):
        client = pymongo.MongoClient(self.MONGODBURI)
        db = client.dota_teamfight_app
        table = db.matches
        table.insert_one({
            "game_id": self.id,
            "matchend": self.matchend,
            "entry_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

        return True

    def retreive_matchend(self):
        client = pymongo.MongoClient(self.MONGODBURI)
        db = client.dota_teamfight_app
        table = db.matches
        sys.stdout.write(('-' * 50))
        print('SEARCHING FOR GAME -- ', self.id)
        r = table.find_one({"game_id": self.id})
        print(r)
        self.matchend = r['matchend']
