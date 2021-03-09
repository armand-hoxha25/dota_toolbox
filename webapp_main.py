import os
from flask import Flask, redirect, url_for, render_template, request
import plotly.express as px
import plotly
import plotly.graph_objects as go
import json

static_dir=os.path.abspath('./templates')
app=Flask(__name__,template_folder=static_dir,static_folder=static_dir)

@app.route("/", methods=['GET','POST'])
def home():
    if request.method== "POST":
        matchid=request.form["matchid"]
        with open("tmp_txt.txt","w+") as f:
            f.write(matchid)
        print("-----------matchid=",matchid,'------------------------')
        graphJSON=get_graphs(matchid)
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

def get_graphs(matchid):
    data=[go.Scatter(x=[1,2,3],y=[1,2,3])]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    print('graph generated')
    return graphJSON

if __name__== "__main__":
    app.run()
    