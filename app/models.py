
# ****************************** models.py *********************************
# Holds all the models that represent objects in our database
# *************************************************************************

from app import db
import steam_requests

#Model for our users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(33))
    nickname = db.Column(db.String(33))
    avatar = db.Column(db.String(4000))

    #Gets a user, if they dont exist create them
    @staticmethod
    def get_or_create(steam_id):
        rv = User.query.filter_by(steam_id=steam_id).first()
        if rv is None:
            rv = User()
            rv.steam_id = steam_id
            db.session.add(rv)
        return rv

    #How User is printed
    def __repr__(self):
        return '<User= id: %d, Steam ID: %s, Nickname: %s>' %(self.id , self.steam_id , self.nickname)


#Model for Games
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steam_app_id = db.Column(db.Integer)
    name = db.Column(db.String(4000))
    image = db.Column(db.String(4000))
    steam_url = db.Column(db.String(4000))

    #Gets a game, if it doesnt exist create it
    @staticmethod
    def get_or_create(steam_app_id):
        rv = Game.query.filter_by(steam_app_id=steam_app_id).first()
        if rv is None:
            rv = Game()
            rv.steam_app_id = steam_app_id
            rv.name = steam_requests.game_name(steam_app_id)
            rv.image = steam_requests.game_image(steam_app_id)
            rv.steam_url = 'http://steamcommunity.com/app/%d' %steam_app_id
            db.session.add(rv)
        return rv

    #How Game is printed
    def __repr__(self):
        return '<Game= name: %s, Steam ID: %d>' %(self.name , self.steam_app_id)

