
# ****************************** steam_requests.py ******************************
# Holds all of our requests that will be sent to the steam api.
# *******************************************************************************

import requests, json, logging, re
from bs4 import BeautifulSoup
from config import STEAM_API_KEY
from flask import jsonify
from app import models
#from models import Game, Tag

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

    wishlist = []
    for appId in games:
        game = Game.get(appId)
        if(game is not None):
            wishlist.append(game)
    return wishlist

# Gets a games info from a steam app id
def game_info(steamAppId, game):
    # game.tags = game.metacritic = game.genres = game.developers = game.publishers = None

    url = 'http://store.steampowered.com/app/%d' %steamAppId
    rv = requests.get(url)
    soup = BeautifulSoup(rv.text)

    desDiv = soup.find("div", class_="game_description_snippet")
    if(desDiv is None): #TODO:Issue #25, We hit the birthdate redirect most likely
        print 'desDiv = None'
        return
    else:
        game.description = desDiv.text.strip()

    #Tags
    tagsDiv = soup.find("div", class_="glance_tags popular_tags")
    if tagsDiv is not None:
        for tag in tagsDiv.find_all("a"):
            tagP = models.Tag.get_or_create(tag.text.strip(), tag['href'])
            game.add_tag(tagP)

    #Metacritic
    metaDiv = soup.find("div", {"id": "game_area_metascore"})
    if metaDiv is not None:
        scoreString = metaDiv.text.strip()
        if "/" in scoreString:
            game.metacritic = int( metaDiv.text.strip().split("/")[0] )
        else:
            game.metacritic = -1

    #Details
    detailsDiv = soup.find("div", class_="details_block")
    if detailsDiv is not None:
        for a in detailsDiv.find_all("a"):
            if "genre" in a['href']:
                genre = models.Genre.get_or_create(a.text.strip(), a['href'])
                game.add_genre(genre)
            elif "developer" in a['href']:
                developer = models.Developer.get_or_create(a.text.strip(), a['href'])
                game.add_developer(developer)
            elif "publisher" in a['href']:
                publisher = models.Publisher.get_or_create(a.text.strip(), a['href'])
                game.add_publisher(publisher)
    return ""


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

# Gets the games a user owns from a steam id
def get_owned_games(steamId):
    params = {
        'key': STEAM_API_KEY,
        'steamid': steamId
    }

    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?'
    rv = requests.get(url, params=params).json()

    games = []
    if(rv['response']['game_count'] != 0):
        for game in rv['response']['games']:
            games.append(game['appid'])

    owned = []
    for appId in games:
        game = Game.get(appId)
        if(game is not None):
            owned.append(game)

    return owned
