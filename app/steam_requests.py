
# ****************************** steam_requests.py ******************************
# Holds all of our requests that will be sent to the steam api.
# *******************************************************************************

import requests, json, logging, re
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
    # url = 'http://store.steampowered.com/app/%d' %steamAppId
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)

    info = []
    # Add the name of the game
    info.append( soup.find('div', {'class':'apphub_AppName'}).text )
    # Add the image
    info.append( soup.find('img', {'class':'apphub_StoreAppLogo'})['src'] )
    # Add the description
    info.append( soup.find('div', {'class':'apphub_StoreAppText'}).text )

    # # Messing with issue#19
    # # Add the name of the game
    # info.append( soup.find('div', {'class':'apphub_AppName'}).text )
    # # Add the image
    # info.append( soup.find('img', {'class':'game_header_image'})['src'] )
    # # Add the description
    # info.append( soup.find('div', {'class':'game_description_snippet'}).text )
    # text = soup.find(id="game_area_description")
    # result = re.search(r'.*(<h2 class="bb_tag">)', str(text))
    # info.append(result.group())
    # info.append(soup.find(id="game_area_description").text )# gets the game description

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
