
# ****************************** twitch_requests.py *****************************
# Holds all of our requests that will be sent to the twitch api.
# *******************************************************************************

import requests, json
from flask import jsonify

# Simply gets the top games on Twitch.TV
def topgames():
    toplist = requests.get('https://api.twitch.tv/kraken/games/top')
    return jsonify(toplist.json())


# Search twitch for a specific game
def searchgame(game):
    url = 'https://api.twitch.tv/kraken/search/streams/?q=%s' %game
    gameSearch = requests.get(url).json()
    if(gameSearch['_total']!=0):

        channel=gameSearch['streams'][0]['channel']['name']
    else:
        channel=""
    return channel


# Search twitch for a specific game
def searchgame(game):
    url = 'https://api.twitch.tv/kraken/search/streams/?q=%s' %game
    gameSearch = requests.get(url).json()
    if(gameSearch['_total'] == 0):
    	channel=""
    elif(gameSearch['streams'] == 0):
    	channel=""
    else:
        channel=gameSearch['streams'][0]['channel']['name']
    return channel
