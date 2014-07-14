
# ****************************** steam_requests.py ******************************
# Holds all of our requests that will be sent to the steam api.
# *******************************************************************************

import requests, json
from bs4 import BeautifulSoup
from config import STEAM_API_KEY
from flask import jsonify

# Get a steam users info
def user_info(steam_id):
    params = {
        'key': STEAM_API_KEY,
        'steamids': steam_id
    }

    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0001/?'
    rv = requests.get(url, params=params).json()
    return rv['response']['players']['player'][0] or {}

# Get a steam users wishlist
def user_wishlist(steam_id):
    url = 'http://steamcommunity.com/profiles/%s/wishlist/' %steam_id
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)
    games =[]
    for game in soup.find_all('div', {'class':'wishlistRow'}):
        games.append(int(game.get('id').strip('game_')))
    return games

# Gets a game image from a steam app id
def game_image(steam_app_id):
    url = 'http://steamcommunity.com/app/%d' %steam_app_id
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)
    image = soup.find('img', {'class':'apphub_StoreAppLogo'})['src']
    return image

# Gets a game name from a steam app id
def game_name(steam_app_id):
    url = 'http://steamcommunity.com/app/%d' %steam_app_id
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)
    name = soup.find('div', {'class':'apphub_AppName'}).text
    return name

# Gets news for a game on steam from a steam app id
def game_news(steam_app_id):
    params = {
        'key': STEAM_API_KEY,
        'appid': steam_app_id,
        'count': 3,
        'maxLength': 4000
    }

    url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?'
    rv = requests.get(url, params=params).json()

    #we need to return something here
    return 'nothing being returned yet'
