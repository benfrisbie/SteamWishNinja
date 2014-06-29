
# ****************************** steam_requests.py ******************************
# Holds all of our requests that will be sent to the steam api.
# *******************************************************************************

import requests, json
from config import STEAM_API_KEY
from flask import jsonify

# Get a steam users info
def userinfo(steam_id):
    options = {
        'key': STEAM_API_KEY,
        'steamids': steam_id
    }
    
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0001/?'
    rv = requests.get(url, params=options).json()
    return rv['response']['players']['player'][0] or {}

# Get a steam users wishlist
def userwishlist(steam_id):
    url = 'http://steamcommunity.com/profiles/%s/wishlist/' %steam_id
    rv = requests.get(url)
    return jsonify(rv.json())
