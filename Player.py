class Player(account_id):
    '''
    The Player class includes all the characteristics of a player.
    Input:
    the Dota Id or the Steam 32 bit ID
    '''

    def __init__(self):
        '''
        Initialize the Player object with default values for placeholders
        '''
        self.nickname=""
        self.matchhistory_json=[]
        self.matchhistory_df=[]
        

    def get_player_match_history(self,account_id):
        '''
        Fetches the last 10,000 matches of the player, and saves it into a pickle file (due to limited
        number of api calls in each month)
        
        Input:
        account_id (int): the Dota Id or the Steam 32 bit ID

        Output:
        matchhistory (dict): a list of dictionaries of each match played with the opendota format
        '''
        api_req='''https://api.opendota.com/api/players/{}/matches?limit=10000&project=heroes'''
        r=requests.get(api_req.format(account_id))
        matchhistory=r.json()
        pickle.dump(matchhistory,open(str(account_id)+'_matches.p','wb'))
        return matchhistory

    # load the json object saved
    matchhistory=pickle.load(open(filepath,'rb'))

    def parse_player_match_history(self,matchhistory):
        '''
        Parses the json data from the match history of a player.

        Input:
        matchhistory: json dictionary type with the format of opendota
        
        Output:
        player_df : pandas dataframe with the following schema
        -- match_ids (int): the unique match id
        -- heroes (int): the unique hero id 
        -- match_length (int): match length in seconds
        -- win (bool): True if player won
        -- team_radiant(bool): True if player was Radiant 

        '''
        ## parse open dota data
        match_ids=[]
        heroes=[]
        match_length=[]
        win=[]
        team_radiant=[] # player_slot < 128 is radiant
        l=len(matchhistory)
        n=0
        for match in matchhistory:
            match_ids.append(match['match_id'])
            playersheroes=list(match['heroes'].values())
            for d in playersheroes:
                try:
                    if d['account_id']==account_id:
                        break
                except KeyError:
                    pass
            heroes.append(d['hero_id'])
            match_length.append(match['duration'])
            win.append(True if match['radiant_win'] and match['player_slot']<128 else False)
            team_radiant.append(True if match['player_slot']<128 else False)
            n+=1
            x=str(n)+'/'+str(l)
            print(f'\r', end="")
            print(f'{x}', end="")
        print(f'\n')

        player_df=pd.DataFrame({'match_ids':match_ids,
        'heroes':heroes,
        'match_length':match_length,
        'win':win,
        'team_radiant':team_radiant})
        return player_df

if __name__=='main':
    #initiate for Fresh Cookies example
    P=Player(78812268)
