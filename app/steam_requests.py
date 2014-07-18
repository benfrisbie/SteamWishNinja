
# ****************************** steam_requests.py ******************************
# Holds all of our requests that will be sent to the steam api.
# *******************************************************************************

import requests, json
from bs4 import BeautifulSoup
from config import STEAM_API_KEY
from flask import jsonify

# Get a steam users info
def user_info(steamId):
    params = {
        'key': STEAM_API_KEY,
        'steamids': steamId
    }

    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0001/?'
    rv = requests.get(url, params=params).json()
    return rv['response']['players']['player'][0] or {}

# Get a steam users wishlist
def user_wishlist(steamId):
    url = 'http://steamcommunity.com/profiles/%s/wishlist/' %steamId
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)
    games =[]
    for game in soup.find_all('div', {'class':'wishlistRow'}):
        games.append(int(game.get('id').strip('game_')))
    return games

# Gets a game info from a steam app id
# Result array format -> [name, image, description]
def game_info(steamAppId):
    url = 'http://steamcommunity.com/app/%d' %steamAppId
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)

    info = []
    # Add the name of the game
    info.append( soup.find('div', {'class':'apphub_AppName'}).text )
    # Add the image
    info.append( soup.find('img', {'class':'apphub_StoreAppLogo'})['src'] )
    # Add the description
    info.append( soup.find('div', {'class':'apphub_StoreAppText'}).text )

    return info

# Gets news for a game on steam from a steam app id
def game_news(steamAppId):
    params = {
        'key': STEAM_API_KEY,
        'appid': steamAppId,
        'count': 3,
        'maxLength': 4000
    }

    url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?'
    rv = requests.get(url, params=params).json()

    #we need to return something here
    return 'nothing being returned yet'
