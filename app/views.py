
# ****************************** views.py *********************************
# Holds all the handlers that will respond to requests from the browser.
# Each python function in here will map to 1 or more request URLs.
# *************************************************************************
import requests
from flask import render_template, redirect, url_for, jsonify
from app import app, oid

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
    return oid.try_login('http://steamcommunity.com/openid')

# Called after a login
@oid.after_login
def create_or_login(resp):
    return 'You signed in!'

# Simply gets the top games on Twitch.TV
@app.route('/topgames')
def topgames():
    toplist=requests.get("https://api.twitch.tv/kraken/games/top")
    return jsonify(toplist.json())
