
# ****************************** views.py *********************************
# Holds all the handlers that will respond to requests from the browser.
# Each python function in here will map to 1 or more request URLs.
# *************************************************************************

import re, requests, json
from urllib import urlencode, quote
from flask import render_template, redirect, flash, url_for, g, session, jsonify
from app import app, oid, db
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
    steamdata = get_steam_userinfo(g.user.steam_id)
    g.user.nickname = steamdata['personaname']
    db.session.commit()
    session['user_id'] = g.user.id
    flash('You are logged in as %s, id: %s' %(g.user.nickname, g.user.steam_id) )
    return redirect(url_for('index'))

#testing this
def get_steam_userinfo(steam_id):
    options = {
        'key': app.config['STEAM_API_KEY'],
        'steamids': steam_id
    }
    # url = 'http://api.steampowered.com/ISteamUser/' \
    #       'GetPlayerSummaries/v0001/?%s' % urllib.urlencode(options)
    # rv = json.load(urllib2.urlopen(url))

    url = 'http://api.steampowered.com/ISteamUser/' \
          'GetPlayerSummaries/v0001/?'
    rv = requests.get(url, params=options).json()
    return rv['response']['players']['player'][0] or {}

# Logs the current user out
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You logged out')
    return redirect(url_for('index'))

# Called before every request to pull in current user
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


# Simply gets the top games on Twitch.TV
@app.route('/topgames')
def topgames():
    toplist=requests.get("https://api.twitch.tv/kraken/games/top")
    return jsonify(toplist.json())
