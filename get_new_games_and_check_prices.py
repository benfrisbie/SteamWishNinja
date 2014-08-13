# ******************************* get_new_games_and_check_prices.py ********************************
# Checks Steam for new games and adds them to the DB. It also checks for pricing updates on all
# at the same time.
# **************************************************************************************************

import requests, logging, re, math
from bs4 import BeautifulSoup
from app import app, models, db

print 'Starting script...'

url = 'http://store.steampowered.com/search/?sort_by=Name&sort_order=ASC&category1=998&page=1'
rv = requests.get(url)
soup = BeautifulSoup(rv.text)

#Find out how many pages there are
entries = soup.find("div", {"class":"search_pagination_left"}).text.strip()
print 'entries: %s' %entries
#TODO: Calcualte number of pages
numGames = int( entries.split(' ')[5] )
numGamesPerPage = int( entries.split(' ')[3] )
numPages = int( math.ceil( numGames / float(numGamesPerPage) ) )

print '%d total games / %d games per page = %d pages' %(numGames, numGamesPerPage, numPages)
print '---------------------------------Page#1------------------------------------'

# Loop through all the pages of games
for page in range(1, numPages+1):
	url = 'http://store.steampowered.com/search/?sort_by=Name&sort_order=ASC&category1=998&page=%d' %page
	rv = requests.get(url)
	soup = BeautifulSoup(rv.text)
	gamesOnPage = soup.findAll("a", {"class":"search_result_row"})

	#Loop through all the games on this page
	for gameDiv in gamesOnPage:
		appId = int( re.search('\d+', gameDiv['href']).group(0) )
		game = models.Game.get(appId)

		priceString = gameDiv.find("div", {"class":"col search_price"}).text.strip('$')

		#TODO:Check if it says 'Free to play'
		if(priceString is None or priceString == '' or priceString.lower() == 'Free to Play'.lower()):
			price = 0			
		elif( len(priceString.split('$')) > 1):
			priceString = priceString.split('$')[1]
			price = int( float(priceString) * 100)
		else:
			price = int( float(priceString) * 100)

		if(game is None): #New game in our DB
			game = models.Game.create(appId)
			
			pricePoint = models.Price(price=price)
			game.add_price(pricePoint)

			print '+ (%d) %s - $%s' %(game.steamAppId, game.name, priceString)

		else: #Game thats already in our DB
			if(price != game.priceCurrent): #Price difference
				pricePoint = models.Price(price=price)
				game.add_price(pricePoint)
				print '* (%d) %s - $%s' %(game.steamAppId, game.name, priceString)
		
	print '---------------------------------Page#%d------------------------------------' %(page+1)
	db.session.commit()

#Double check and commit changes to DB
db.session.commit()


