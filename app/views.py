
# ****************************** views.py *********************************
# Holds all the handlers that will respond to requests from the browser.
# Each python function in here will map to 1 or more request URLs.
# *************************************************************************

import re, requests, json, steam_requests, twitch_requests
from flask import render_template, redirect, flash, url_for, g, session, jsonify
from app import app, oid, db, models
from models import User, Game


# The first page/home that will be displayed first
# routed to both the views
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')


# Log in a user using Steam OpenID
@app.route('/login')
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    return oid.try_login('http://steamcommunity.com/openid')


# Called after a login
@oid.after_login
def create_or_login(resp):
    _steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')
    match = _steam_id_re.search(resp.identity_url)
    g.user = User.get_or_create(match.group(1))
    steamdata = steam_requests.user_info(g.user.steam_id)
    g.user.nickname = steamdata['personaname']
    g.user.avatar = steamdata['avatarfull']
    db.session.commit()
    session['user_id'] = g.user.id
    flash('You logged in as %s' %g.user.nickname )
    return redirect(url_for('user', nickname = g.user.nickname))


# Called before every request to pull in current user
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


# Logs the current user out
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You logged out')
    return redirect(url_for('index'))


# user profile page
@app.route('/user/<nickname>')
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User with SteamID: ' + nickname + ' not found.')
        return redirect(url_for('index'))

    wishlist_ids = steam_requests.user_wishlist(user.steam_id)

    wishlist = []
    for app_id in wishlist_ids:
        game = Game.get_or_create(app_id)
        wishlist.append(game)

    db.session.commit()

    return render_template('user.html', user = user, wishlist = wishlist)


# Page for a game and all the info on it
@app.route('/game/<steam_app_id>')
def game(steam_app_id):
    # Get the gameId on steam here
    game = Game.query.filter_by(steam_app_id = steam_app_id).first()
    game_streams = twitch_requests.searchgame(game.name) # need to return an embeded url to display as test

    return render_template('game.html', game = game, game_streams = game_streams)


# Page for the top games on Twitch
@app.route('/topgamesontwitch')
def topgamesontwitch():
    return twitch_requests.topgames()


# Returns a list of all the users in our db
@app.route('/userlist')
def userlist():
    users = models.User.query.all()
    return render_template('users.html', users = users)
