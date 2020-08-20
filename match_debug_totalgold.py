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
            timestamp_r.append(str_time_to_sec(last_timestamp))
    
    elif l[0:4]==" Dir":
        myline=l.split(',')[1:]
        if myline !=[]:
           dire_lines.append(myline)
           timestamp_d.append(str_time_to_sec(last_timestamp))

heroes=['invoker',
 'disruptor',
 'enigma',
 'tusk',
 'antimage',
 'crystal_maiden',
 'drow_ranger',
 'bounty_hunter',
 'rattletrap',
 'nevermore']

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