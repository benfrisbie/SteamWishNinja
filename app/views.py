
# ****************************** views.py *********************************
# Holds all the handlers that will respond to requests from the browser.
# Each python function in here will map to 1 or more request URLs.
# *************************************************************************
from flask import render_template, redirect, url_for, g
from app import app, oid
import re

_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

# The first page/home that will be displayed first
# routed to both the views
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')


# log in a user using Steam OpenID
@app.route('/login')
@oid.loginhandler
def login():
    return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def create_or_login(resp):
    return 'You signed in!'