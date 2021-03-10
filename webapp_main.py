import os
from flask import Flask, redirect, url_for, render_template, request
import plotly.express as px
import plotly
import plotly.graph_objects as go
import json
from match_parsers import parse_matchinfo
from match_parsers import parse_networth

static_dir=os.path.abspath('./templates')
app=Flask(__name__,template_folder=static_dir,static_folder=static_dir)

@app.route("/", methods=['GET','POST'])
def home():
    if request.method== "POST":
        matchid=request.form["matchid"]
        with open("tmp_txt.txt","w+") as f:
            f.write(matchid)
        print("-----------Parsing matchid=",matchid,'------------------------')
    
        matchinfo_file="./test_files/temp_info.txt"
        print("Running on test script, Printing final output dataframe")
        matchinfo=parse_matchinfo(matchinfo_file)
        print(matchinfo.head())

        combat_file="./test_files/temp_combat.txt"
        Radiant,Dire=parse_networth(combat_file,matchinfo)
        
        graphJSON=get_graphs(Radiant,Dire)

        return  render_template("index_dash.html",matchid=matchid,graphJSON=graphJSON)
    else:
        return render_template("index.html", template_folder='templates')
    return render_template("index.html", template_folder='templates', matchid=matchid)

@app.route("/match",methods=["POST","GET"])
def get_match():
    if request.method== "GET":
        matchid=request.form["matchid"]
        with open("tmp_txt.txt","w+") as f:
            f.write(matchid)
        print("-----------matchid--------------------")
        return  f"<h1>{matchid}</h1>"
    else:
        return render_template("index_dash.html",matchid=matchid)
@app.route("/<matchid>")
def match(matchid):
    return f"<h1>{matchid}</h1>"

def get_graphs(Radiant,Dire):

    data=[]
    for h in Radiant.columns:
        if h=='timestamp':
            continue
        data.append(go.Scatter(x=Radiant['timestamp']/60,y=Radiant[h], name=h))

    layout={'title':'Radiant Net Worth',
                  'xaxis':{'title':'time (min)'},
                  'yaxis':{'title':'Gold'},
                  
                  }

    graph={'data':data,'layout':layout}
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    print('graph generated')
    return graphJSON

if __name__== "__main__":
    app.run()
    