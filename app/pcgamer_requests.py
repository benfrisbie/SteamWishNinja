# ****************************** pcgamer_requests.py ****************************
# *                     because fuck API's and fuck PCGamer                     *
# *******************************************************************************

import requests, json
from flask import jsonify
from bs4 import BeautifulSoup

# baseUrl="http://www.pcgamer.com/search/%s"

def searchPcGame(game):
    #need to parse id="search_items"
    url = 'http://www.pcgamer.com/search/%s' %game
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)
    zz = soup.find_all(id="search_items")
    # zzSoup = BeautifulSoup(zz.text)
    # foo = []
    # foo.append(articlesSoup)
    return zz
