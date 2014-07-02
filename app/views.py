
# ****************************** views.py *********************************
# Holds all the handlers that will respond to requests from the browser.
# Each python function in here will map to 1 or more request URLs.
# *************************************************************************

import re, requests, json, steam_requests, twitch_requests
from flask import render_template, redirect, flash, url_for, g, session, jsonify
from app import app, oid, db, models
from models import User


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
    steamdata = steam_requests.userinfo(g.user.steam_id)
    g.user.nickname = steamdata['personaname']
    g.user.avatar = steamdata['avatarfull']
    db.session.commit()
    session['user_id'] = g.user.id
    flash('You logged in as %s, id: %s' %(g.user.nickname, g.user.steam_id) )
    return redirect(url_for('user', steam_id = g.user.steam_id))


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
@app.route('/user/<steam_id>')
def user(steam_id):
    user = User.query.filter_by(steam_id = steam_id).first()
    if user == None:
        flash('User with SteamID: ' + steam_id + ' not found.')
        return redirect(url_for('index'))

    wishlist = steam_requests.userwishlist(g.user.steam_id)
    return render_template('user.html', user = user, wishlist = wishlist)


# Page for a game and all the info on it
@app.route('/game/<game_name>')
def game(game_name):
    return render_template('game.html', game_name = game_name)


# Page for the top games on Twitch
@app.route('/topgamesontwitch')
def topgamesontwitch():
    return twitch_requests.topgames()


# @app.route('/userlist')
# def userlist():
#     allusers = models.User.query.all()
#     return jsonify(alluser)
