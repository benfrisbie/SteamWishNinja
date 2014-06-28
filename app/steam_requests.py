
# ****************************** steam_requests.py ******************************
# Holds all of our requests that will be sent to the steam api.
# *******************************************************************************

import requests, json
from config import STEAM_API_KEY

# Get a steam users info
def get_steam_userinfo(steam_id):
    options = {
        'key': STEAM_API_KEY,
        'steamids': steam_id
    }
    
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0001/?'
    rv = requests.get(url, params=options).json()
    return rv['response']['players']['player'][0] or {}
