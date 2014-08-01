
# ****************************** twitch_requests.py *****************************
# Holds all of our requests that will be sent to the twitch api.
# *******************************************************************************

import requests, json, logging
from flask import jsonify
logging.basicConfig(filename='output.log',level=logging.DEBUG)

# Simply gets the top games on Twitch.TV
def topgames():
    toplist = requests.get('https://api.twitch.tv/kraken/games/top')
    return jsonify(toplist.json())


# Search twitch for a specific game
def searchgame(game):
    params = {
        'game': game,
        'limit': 1
    }

    url = 'https://api.twitch.tv/kraken/streams/?'
    gameSearch = requests.get(url, params=params).json()
    logging.warning(gameSearch)
    if(gameSearch['_total'] == 0):
    	channel=""
      logging.warning(game + " has no streams.")
    elif(gameSearch['streams'] == 0):
    	channel=""
    else:
        channel=gameSearch['streams'][0]['channel']['name']
    return channel
