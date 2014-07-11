
# ****************************** steam_requests.py ******************************
# Holds all of our requests that will be sent to the steam api.
# *******************************************************************************

import requests, json
from bs4 import BeautifulSoup
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
    soup=BeautifulSoup(rv.text)
    games =[]
    for game in soup.find_all('div', {'class':'wishlistRow'}):
        games.append(int(game.get('id').strip('game_')))
    return games

# Get a games image
def getgameimage(gameId):
    url = 'http://steamcommunity.com/app/%d' %gameId
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)
    image = soup.find('img', {'class':'apphub_StoreAppLogo'})['src']
    return image

def getgamename(gameId):
    url = 'http://steamcommunity.com/app/%d' %gameId
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)
    name = soup.find('div', {'class':'apphub_AppName'}).text
    return name