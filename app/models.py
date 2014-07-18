
# ****************************** models.py *********************************
# Holds all the models that represent objects in our database
# *************************************************************************

from app import db
import steam_requests

#Model for our users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steamId = db.Column(db.String(33))
    nickname = db.Column(db.String(33))
    avatar = db.Column(db.String(4000))

    #Gets a user, if they dont exist create them
    @staticmethod
    def get_or_create(steamId):
        rv = User.query.filter_by(steamId = steamId).first()
        if rv is None:
            rv = User()
            rv.steamId = steamId
            db.session.add(rv)
        return rv

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

    #Gets a game, if it doesnt exist create it
    @staticmethod
    def get_or_create(steamAppId):
        rv = Game.query.filter_by(steamAppId = steamAppId).first()
        if rv is None:
            rv = Game()
            rv.steamAppId = steamAppId
            info = steam_requests.game_info(steamAppId)
            rv.name = info[0]
            rv.image = info[1]
            rv.description = info[2]
            rv.steamUrl = 'http://steamcommunity.com/app/%d' %steamAppId
            db.session.add(rv)
        return rv

    #How Game is printed
    def __repr__(self):
        return '<Game= name: %s, Steam ID: %d>' %(self.name , self.steamAppId)

