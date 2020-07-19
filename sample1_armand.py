#%% library import
from steam.client import SteamClient
from dota2.client import Dota2Client
import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)

client = SteamClient()
dota = Dota2Client(client)
print("hello")
@client.on('logged_on')
def status_logged():
    print('WE ARE LOGGED ON')

@dota.on('ready')
def do_dota_stuff():
    print("the game is ready")

client.cli_login()
client.run_forever()

#start_dota()
print('life')

@dota.on('my event')
def do_stuff(a, b):
    print "Hey!"

dota.on('my event', do_stuff)
dota.once('my event', do_stuff)  # call do_stuff just one time
dota.wait_event('my event')      # blocks and returns arguments, if any


dota.emit("my event")
dota.emit("my event", 1, [3,4,5])  # optional arguments
