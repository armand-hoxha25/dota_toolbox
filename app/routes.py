from dota_toolbox import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import (
    search_game,
)
#from app.models import User, Post
#from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.models import Match
import sys


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = search_game(request.form)
    if request.method == 'POST':
        #matchid = form['gameid']
        sys.stdout.write('POST submitted \n')

    if form.validate():
        print('we just submitted!!')
        matchid = form.searchfield.data
        sys.stdout.write('----matchid = {}'.format(matchid))
        match = Match(matchid)
        if match.match_in_db():
            return redirect(url_for('match', matchid=matchid))
        else:
            match.get_match_file_url()
            if match.status == 'no_download':
                return render_template('index.html', form=form, page='home',
                                       message='Cannot find match, try another match')
            match.fetch_match()
            if match.status == 'no_download':
                return render_template('index.html', form=form, page='home',
                                       message='Cannot find match, try another match')
            match.parse_match()
            match.matchend_jsonify()
            match.insert_in_db()
            match.retreive_matchend()
            return redirect(url_for('match', matchid=match.id))
    return render_template('index.html', form=form, page='home')


@app.route('/match/<matchid>', methods=['GET', 'POST'])
def match(matchid):
    match = Match(matchid)
    match.retreive_matchend()
    form = search_game(request.form)
    if request.method == 'POST':
        #matchid = form['gameid']
        print('here we go?')
        print(request.form)
        print(form.searchfield)
        print(form.validate())
        print(form.errors)
        if form.validate():
            print('we just submitted!!')
            matchid = form.searchfield.data
            print('----matchid = {}'.format(matchid))
            match = Match(matchid)
            if match.match_in_db():
                return redirect(url_for('match', matchid=matchid, matchend=matchid, form=form))
            else:
                match.get_match_file_url()
                if match.status == 'no_download':
                    return render_template('index.html', form=form, page='home',
                                           message='Cannot find match, try another match')
                match.fetch_match()
                if match.status == 'no_download':
                    return render_template('index.html', form=form, page='home',
                                           message='Cannot find match, try another match')
                match.parse_match()
                match.matchend_jsonify()
                match.insert_in_db()
                match.retreive_matchend()
                return redirect(url_for('match', matchid=match.id))
    return render_template('match.html', matchend=match.matchend, form=form)
