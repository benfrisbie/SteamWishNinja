# ****************************** pcgamer_requests.py ****************************
# *                     because fuck API's and fuck PCGamer                     *
# *******************************************************************************

import requests, json
from flask import jsonify
from bs4 import BeautifulSoup
import logging
logging.basicConfig(filename='output.log',level=logging.WARNING)

# baseUrl="http://www.pcgamer.com/search/%s"

def searchPcGame(game):
    #need to parse id="search_items"
    url = 'http://www.pcgamer.com/search/%s' %game
    rv = requests.get(url)
    soup=BeautifulSoup(rv.text)
    zz = soup.find_all(id="search_items")
    titles = [a.get_text() for a in soup.find_all('h3')]
    # zzSoup = BeautifulSoup(zz.text)
    # foo = []
    # foo.append(articlesSoup)
    # return titles
    return zz
