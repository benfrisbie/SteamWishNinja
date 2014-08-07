# ******************************* priceGetter.py ********************************
# Gets the prices for games 'Straight outta Compton'
# *******************************************************************************

import requests, json, logging, re
from bs4 import BeautifulSoup

#this function will get the price of a steam game by scraping the steam page
def price_cron(steamAppId):
  url = 'http://store.steampowered.com/app/%d' %steamAppId
  rv = requests.get(url)
  soup=BeautifulSoup(rv.text)
  priceArray=soup.findAll("div", {"class":"game_purchase_price"})  #this will create an array
  price = priceArray[0].text  #slims down from string to array
  price=price.strip() #removes white spaces && tabs && newlines 
