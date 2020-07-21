import requests as r
import time
import datetime as dt
from bs4 import BeautifulSoup
key= None

with open("dota2_apikey.txt",'r') as kd:
    key=kd.readlines()[0]

match_api_base='https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key={}'

#%% simple get last 25 matches api request
req=r.get(match_api_base.format(key))
match_history_in_json=req.json()


# %% requst by player name
by_match='https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?matches_requested=1_&account_id={}_&key={}'

player_name='76561198089787694'
req=r.get(by_match.format(player_name,key))
jreq=req.json()
matchdata=jreq['result']['matches'][0]
frmt_date = dt.datetime.utcfromtimestamp(matchdata['start_time']).strftime("%Y/%m/%d %H:%M")

print(req.json())
# time comes back in epoch time, which is not that useful

## get account names (if we can)
# https://steamid.xyz/76561198089787694 where 76561198089787694 is the account id
def get_name(id):
    '''
    searches through the steamid.xyz and scrapes the name
    id: (str) steam id of the user to be searched
    
    returns name (str)
    '''
    page=r.get("https://steamid.xyz/{}".format(id))
#bsoup=BeautifulSoup(page.content,'html.parser')
#soup_list=list(bsoup.children)
    txt=page.text
    template_string='''Nick Name\r\n<input type="text" onclick="this.select();" value="'''
    template_end='''">\r\nProfile URL\r\n<input type="text'''
    pad=len(template_string)
    start=txt.find(template_string)
    end=txt.find(template_end)
    ## find the end of the name
    if start ==-1:
        return "Unkown"
    attempt1=txt[start+pad:end]
    return attempt1

players=matchdata['players']

player_names=[get_name(str(p['account_id'])) for p in players]
print(player_names)
#%%
'''STRATZ API '''
api_base='https://api.stratz.com'


