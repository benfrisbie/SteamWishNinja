
# ****************************** models.py *********************************
# Holds all the models that represent objects in our database
# *************************************************************************

from app import db
import steam_requests
import datetime

#Model for our users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steamId = db.Column(db.String(33))
    nickname = db.Column(db.String(33))
    avatar = db.Column(db.String(4000))

    #Gets a user
    @staticmethod
    def get(steamId):
        return User.query.filter_by(steamId = steamId).first()

    #Create a user
    @staticmethod
    def create(steamId):
        user = User()
        user.steamId = steamId
        steamdata = steam_requests.user_info(steamId)
        user.nickname = steamdata['personaname']
        user.avatar = steamdata['avatarfull']
        db.session.add(user)
        db.session.commit()
        return user

    #Update a user
    def update(self):
        steamdata = steam_requests.user_info(self.steamId)
        if(self.nickname != steamdata['personaname'] or self.avatar != steamdata['avatarfull']):
            self.nickname = steamdata['personaname']
            self.avatar = steamdata['avatarfull']
            db.session.commit()
        return self

    #How User is printed
    def __repr__(self):
        return '<User= id: %d, Steam ID: %s, Nickname: %s>' %(self.id , self.steamId , self.nickname)


#Model for Games
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steamAppId = db.Column(db.Integer)
    name = db.Column(db.String(4000))
    image = db.Column(db.String(4000))
    steamUrl = db.Column(db.String(4000))
    description = db.Column(db.String(4000))
    priceCurrent = db.Column(db.Integer)
    prices = db.relationship('Price', backref='game', lazy='dynamic')

    #Gets a game
    @staticmethod
    def get(steamAppId):
        return Game.query.filter_by(steamAppId = steamAppId).first()

    #Create a game
    @staticmethod
    def create(steamAppId):
        game = Game()
        game.steamAppId = steamAppId
        info = steam_requests.game_info(steamAppId)
        game.name = info[0]
        game.image = info[1]
        game.description = info[2]
        game.steamUrl = 'http://steamcommunity.com/app/%d' %steamAppId
        db.session.add(game)
        return game

    #Update a game
    def update(self):
        info = steam_requests.game_info(self.steamAppId)
        game.name = info[0]
        game.image = info[1]
        game.description = info[2]
        db.session.add(game)
        return game

    #Remove a game
    def remove(self):
        db.session.remove(self)

    #Adds a price point to this game
    def add_price(self, price):
        self.priceCurrent = price.price
        self.prices.append(price)
        db.session.merge(self)
        return self

    #How Game is printed
    def __repr__(self):
        return '<Game= name: %s, Steam ID: %d>' %(self.name , self.steamAppId)



#Model for price point on a game
class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steamAppId = db.Column(db.Integer, db.ForeignKey('game.steamAppId'))
    price = db.Column(db.Integer)
    ts = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    #How Price is printed
    def __repr__(self):
        return '<Price= appId: %s, price: %d, ts: %s>' %(self.steamAppId , self.price, str(self.ts))

