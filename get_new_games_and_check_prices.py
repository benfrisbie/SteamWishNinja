# ******************************* get_new_games_and_check_prices.py ********************************
# Checks Steam for new games and adds them to the DB. It also checks for pricing updates on all
# at the same time.
# **************************************************************************************************

import requests, logging, re, math, datetime, sys
from bs4 import BeautifulSoup
from app import app, models, db

url = 'http://store.steampowered.com/search/?sort_by=Name&sort_order=ASC&category1=998&page=1'
rv = requests.get(url)
soup = BeautifulSoup(rv.text)

#Find out how many pages there are
entries = soup.find("div", {"class":"search_pagination_left"}).text.strip()
numGames = int( entries.split(' ')[5] )
numGamesPerPage = int( entries.split(' ')[3] )
numPages = int( math.ceil( numGames / float(numGamesPerPage) ) )

print '*******************************************************************************'
print datetime.datetime.now()
print '%d total games / %d games per page = %d pages' %(numGames, numGamesPerPage, numPages)
print '*******************************************************************************'

# Loop through all the pages of games
for page in range(1, numPages+1):
	print '>>Page#%d<<' %(page)

	url = 'http://store.steampowered.com/search/?sort_by=Name&sort_order=ASC&category1=998&page=%d' %page
	rv = requests.get(url)
	soup = BeautifulSoup(rv.text)
	gamesOnPage = soup.findAll("a", {"class":"search_result_row"})

	#Loop through all the games on this page
	for gameDiv in gamesOnPage:
		appId = int( re.search('\d+', gameDiv['href']).group(0) )
		game = models.Game.get(appId)

		priceDiv = gameDiv.find("div", class_="col search_price ")
		if(priceDiv is None):
			priceDiv = gameDiv.find("div", class_="col search_price discounted")
		priceString = priceDiv.text.strip('$')

		#Parse the price
		m = re.findall('\d+.\d+', priceString)
		if(len(m) == 0):
			price = 0			
		else:
			try:
				price = round(float(m[len(m)-1]) * 100, 0)
			except ValueError:
				price = 0;

		if(game is None): #New game in our DB
			name = gameDiv.find("div", class_="col search_name ellipsis").text.strip()
			game = models.Game.create(appId, name)
			pricePoint = models.Price(price=price)
			game.add_price(pricePoint)

			print '+ (%d) %s - $%s' %(game.steamAppId, game.name, price / float(100))

		else: #Game thats already in our DB
			if(price != game.priceCurrent): #Price difference
				pricePoint = models.Price(price=price)
				game.add_price(pricePoint)
				print '~ (%d) %s - $%s' %(game.steamAppId, game.name, price / float(100))

print ''
#Commit changes to DB
db.session.commit()


