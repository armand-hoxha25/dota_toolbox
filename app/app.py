from flask import Flask, request, jsonify
import time
import datetime
import sys
from flask_cors import CORS, cross_origin
import json
import requests
import os
import subprocess
import bz2
import pprint
import pymongo
import shutil
print(os.getcwd())
coreapp = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(coreapp)
#coreapp.config['DEBUG'] = True

# if __name__ == "__main___":
coreapp.run(host='localhost', debug=False,
            port=os.environ.get('PORT', 3000))


@coreapp.route('/')
@cross_origin()
def index():
    # print(os.getcwd())
    # return 'hello world'
    return coreapp.send_static_file('../build/index.html')
    # return 1


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@coreapp.route('/time')
def get_current_time():
    return {'time': time.time()}


@coreapp.route('/game')
def get_game(game_id):
    f = open("/games/"+game_id + '.json')
    return f


@coreapp.route('/download_game')
def download_game(game_id):
    url = get_match_file_url(game_id)


@coreapp.route('/post_test', methods=['POST'])
def print_post():
    print('print post called!!!')
    game_id = request.get_json()['gameid']
    if match_in_db(game_id):
        print("match found in database")
        r = retreive_matchend(game_id)
        return r, 200

    print('received match : ', game_id)
    replay_url = get_match_file_url(game_id)
    fetch_match(replay_url, game_id)

    print('----- PARSING MATCH ------')
    matchend = parse_match(game_id)
    print('PARSE COMPLETE')
    os.remove('temp/'+game_id+'.dem')
    # f = open("games/" + game_id + "_matchend.txt", "r")
    # text = f.read()
    ret = {"result": matchend_jsonify(matchend)}
    insert_in_db(game_id, ret)

    print(ret)
    return jsonify(ret), 200


def fetch_match(replay_url, matchid):
    '''
    Fetch the match from the dota 2 server.
    '''
    r = requests.get(replay_url)
    print("Match downloaded")
    decompressed = bz2.decompress(r.content)
    print('decompressing ...')
    open('./temp/' + matchid + '.dem', 'wb').write(decompressed)
    print('saving as '+matchid+'.dem')
    return True


def get_match_file_url(matchid):
    ''' fetch the full url from opendota for the match file, somehow opendota has it, idk how
    '''
    print('getting match URL')
    odotapage = requests.get(
        "https://api.opendota.com/api/matches/{} ".format(matchid))
    replay_url = odotapage.json()['replay_url']
    print('URL received: ', replay_url)
    return replay_url


def parse_match(matchid):

    out_combat = os.path.join(os.path.dirname(
        __file__), "games", matchid+"_combat.txt")
    # out_info = os.path.join(os.path.dirname(__file__),
    #                        "games", matchid+"_info.txt")
    # out_lifestate = os.path.join(os.path.dirname(
    #   __file__), "games", matchid + "_lifestate.txt")
    out_matchend = os.path.join(os.path.dirname(
        __file__), "games", matchid+"_matchend.txt")

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
                                'mac_claritys/matchend.one-jar.jar' + " temp/"+matchid+'.dem',
                                shell=True).decode(sys.stdout.encoding)
    # print(s)
    return s


def matchend_jsonify(s):
    """
    game_id(int): the number of the game. 
    find the game record, and conver it to a json format from txt.
    """
    # print(s)
    s = s.replace('│', "--SEPERATOR--")
    text = s.split('\n')
    print(text)
    print(len(text))
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
    return result


# ['name': remdash[1],
#  'level': remdash[3],
#  'K': remdash[5],
#  'D': remdash[7],
#  'A': remdash[9],
#  'Gold': remdash[11],
#  'LH': remdash[13],
#  'Denies': remdash[15]]

def match_in_db(game_id):
    mongo_uri = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(mongo_uri)
    db = client.dota_teamfight_app
    table = db.matches
    r = table.find_one({"game_id": game_id})
    print(r)
    if r == None:
        return False
    else:
        return True


def insert_in_db(game_id, matchend):
    mongo_uri = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(mongo_uri)
    db = client.dota_teamfight_app
    table = db.matches
    table.insert_one({
        "game_id": game_id,
        "matchend": matchend,
        "entry_time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

    return True


def retreive_matchend(game_id):
    mongo_uri = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(mongo_uri)
    db = client.dota_teamfight_app
    table = db.matches
    r = table.find_one({"game_id": game_id})
    print(r)
    return r['matchend']
