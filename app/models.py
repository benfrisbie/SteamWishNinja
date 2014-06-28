
# ****************************** models.py *********************************
# Holds all the models that represent objects in our database
# *************************************************************************

from app import db

#Model for our users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(40))
    nickname = db.Column(db.String(80))

    #Gets a user, if they dont exist create them
    @staticmethod
    def get_or_create(steam_id):
        rv = User.query.filter_by(steam_id=steam_id).first()
        if rv is None:
            rv = User()
            rv.steam_id = steam_id
            db.session.add(rv)
        return rv

    #Check to see if user is null for templating
    def is_null(self):
        if self is None:
            return True
        return False

    #How User is printed, for debugging
    def __repr__(self):
        return '<User #%d, Steam ID: %s, Nickname: %s>' %(self.id , self.steam_id , self.nickname)
