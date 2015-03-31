
# ****************************** views.py *********************************
# Holds all the handlers that will respond to requests from the browser.
# Each python function in here will map to 1 or more request URLs.
# *************************************************************************

import re, requests, json, steam_requests, twitch_requests, youtube_requests, pcgamer_requests, logging, datetime
from flask import render_template, redirect, flash, url_for, g, session, jsonify
from app import app, oid, db, models
from forms import SearchForm
from models import User, Game
from sqlalchemy import func
logging.basicConfig(filename='output.log',level=logging.WARNING)


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
    steamIdRe = re.compile('steamcommunity.com/openid/id/(.*?)$')
    match = steamIdRe.search(resp.identity_url)
    g.user = User.get(match.group(1))
    if(g.user is None):
        g.user = User.create(match.group(1))
    else:
        g.user = g.user.update()

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

    # Check to see it's an actual user in our db
    if user == None:
        flash('User: ' + nickname + ' not found.')
        return redirect(url_for('index'))

    wishlist = steam_requests.user_wishlist(user.steamId)

    owned = steam_requests.get_owned_games(user.steamId)

    return render_template('user.html', user=user, wishlist=wishlist, owned=owned)


# Page for a game and all the info on it
@app.route('/game/<steamAppId>')
def game(steamAppId):
    # Get the gameId on steam here
    game = Game.query.filter_by(steamAppId = steamAppId).first()

    # Check to see it's an actual game in our db
    if(game is None):
        flash('Game: ' + steamAppId + ' not found.')
        return redirect(url_for('index'))

    #All the resources to be displayed
    twitchStream = twitch_requests.searchgame(game.name)
    ytVideos = youtube_requests.search_videos(game)
    #pcArticle = pcgamer_requests.searchPcGame(game.name)


    #Add price history
    priceData = []
    priceDate = []
    for price in game.prices:
        priceData.append( price.price / float(100) )
        priceDate.append( (price.ts.month, price.ts.day, price.ts.year) )

    #Add the current price to the end
    priceData.append( game.priceCurrent / float(100) )
    now = datetime.datetime.utcnow()
    priceDate.append( (now.month, now.day, now.year) )


    return render_template('game.html', game=game, twitchStream=twitchStream, ytVideos=ytVideos, priceData=priceData, priceDate=priceDate)


# Page for the top games on Twitch
@app.route('/topgamesontwitch')
def topgamesontwitch():
    return twitch_requests.topgames()


# Returns a list of all the users in our db
@app.route('/userlist')
def userlist():
    users = User.query.all()
    return render_template('users.html', users = users)


# Returns a list of random games
@app.route('/randomgames')
def randomgames():
    games = Game.query.order_by(func.random()).limit(20)
    return render_template('randomgames.html', games = games)

@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    searchString = form.search.data

    if(searchString is None):
        flash('Search bar was empty. You have to search for something.')
        return redirect(url_for('index'))

    searchString = searchString.lower()
    
    games = Game.query.filter(Game.name.like('%'+searchString+'%'))
    users = User.query.filter(User.nickname.like('%'+searchString+'%'))
  
    return render_template('search.html', games=games, users=users)


# Page not found 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
