
# ****************************** twitch_requests.py *****************************
# Holds all of our requests that will be sent to the twitch api.
# *******************************************************************************

import requests, json
from flask import jsonify

# Simply gets the top games on Twitch.TV
def topgames():
    toplist=requests.get('https://api.twitch.tv/kraken/games/top')
    return jsonify(toplist.json())
