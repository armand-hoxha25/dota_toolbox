import os
from flask import Flask, redirect, url_for, render_template, request
static_dir=os.path.abspath('./templates')
app=Flask(__name__,template_folder=static_dir,static_folder=static_dir)

@app.route("/", methods=['GET','POST'])
def home():
    if request.method== "POST":
        matchid=request.form["matchid"]
        with open("tmp_txt.txt","w+") as f:
            f.write("OMG!!!")
        print("-----------matchid=",matchid,'------------------------')
        return  f"<h1>{matchid}</h1>"
    else:
        return render_template("index.html", template_folder='templates')
    return render_template("index.html", template_folder='templates')

@app.route("/match",methods=["POST","GET"])
def get_match():
    if request.method== "GET":
        matchid=request.form["matchid"]
        with open("tmp_txt.txt","w+") as f:
            f.write("OMG!!!")
        print("-----------matchid--------------------")
        return  f"<h1>{matchid}</h1>"
    else:
        return render_template("index_dash.html")
@app.route("/<matchid>")
def match(matchid):
    return f"<h1>{matchid}</h1>"

if __name__== "__main__":
    app.run()
    