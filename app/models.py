
# ****************************** models.py *********************************
# Holds all the models that represent objects in our database
# *************************************************************************

from app import db
import steam_requests
import datetime

#Many to Many table for tags
tagged = db.Table('tagged',
            db.Column('game_id', db.Integer, db.ForeignKey('game.steamAppId')),
            db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
        )

#Many to Many table for genres
genred = db.Table('genred',
            db.Column('game_id', db.Integer, db.ForeignKey('game.steamAppId')),
            db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
        )

#Many to Many table for developers
developed = db.Table('developed',
            db.Column('game_id', db.Integer, db.ForeignKey('game.steamAppId')),
            db.Column('developer_id', db.Integer, db.ForeignKey('developer.id'))
        )

#Many to Many table for published
published = db.Table('published',
            db.Column('game_id', db.Integer, db.ForeignKey('game.steamAppId')),
            db.Column('publisher_id', db.Integer, db.ForeignKey('publisher.id'))
        )


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
    name = db.Column(db.String(200))
    image = db.Column(db.String(100))
    url = db.Column(db.String(100))
    description = db.Column(db.String(4000))
    priceCurrent = db.Column(db.Integer)
    metacritic = db.Column(db.Integer)
    prices = db.relationship('Price', backref='pricegame', lazy='dynamic')
    tags = db.relationship('Tag', secondary = tagged, backref = db.backref('tags', lazy = 'dynamic'))
    genres = db.relationship('Genre', secondary = genred, backref = db.backref('genres', lazy = 'dynamic'))
    developers = db.relationship('Developer', secondary = developed, backref = db.backref('developers', lazy = 'dynamic'))
    publishers = db.relationship('Publisher', secondary = published, backref = db.backref('publishers', lazy = 'dynamic'))


    #Gets a game
    @staticmethod
    def get(steamAppId):
        return Game.query.filter_by(steamAppId = steamAppId).first()

    #Create a game
    @staticmethod
    def create(steamAppId, name):
        game = Game()
        game.steamAppId = steamAppId
        game.name = name
        game.image = 'http://cdn.akamai.steamstatic.com/steam/apps/%d/header.jpg' %steamAppId
        game.url = 'http://store.steampowered.com/app/%d' %steamAppId
        db.session.add(game)

        steam_requests.game_info(steamAppId, game)

        return game

    #Update a game
    def update(self):
        #TODO
        return game

    #Remove a game
    def remove(self):
        db.session.remove(self)

    #Adds a price point to this game
    def add_price(self, price):
        self.priceCurrent = price.price
        self.prices.append(price)
        return self

    #Adds a tag to this game
    def add_tag(self, tag):
        self.tags.append(tag)
        return self

    #Adds a tag to this game
    def add_genre(self, genre):
        self.genres.append(genre)
        return self

    #Adds a tag to this game
    def add_developer(self, developer):
        self.developers.append(developer)
        return self

        #Adds a tag to this game
    def add_publisher(self, publisher):
        self.publishers.append(publisher)
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


#Model for a tag
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(200))
    url = db.Column(db.String(200))

    @staticmethod
    def get_or_create(info, url):
        tag =  Tag.query.filter_by(info = info).first()
        if tag is None:
            tag = Tag(info=info, url=url)
            db.session.add(tag)
        return tag

#Model for a genre
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(200))
    url = db.Column(db.String(200))

    @staticmethod
    def get_or_create(info, url):
        genre =  Genre.query.filter_by(info = info).first()
        if genre is None:
            genre = Genre(info=info, url=url)
            db.session.add(genre)
        return genre

#Model for a developer
class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(200))
    url = db.Column(db.String(200))

    @staticmethod
    def get_or_create(info, url):
        developer =  Developer.query.filter_by(info = info).first()
        if developer is None:
            developer = Developer(info=info, url=url)
            db.session.add(developer)
        return developer

#Model for a publisher
class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(200))
    url = db.Column(db.String(200))

    @staticmethod
    def get_or_create(info, url):
        publisher =  Publisher.query.filter_by(info = info).first()
        if publisher is None:
            publisher = Publisher(info=info, url=url)
            db.session.add(publisher)
        return publisher
