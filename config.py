import os

#statement for enabling the development environment
DEBUG = True

#THIS IS SECRET!!
SECRET_KEY = 'super-secret-password'

#Steam API key
STEAM_API_KEY = '6540575332D180142AEBDDCB539005B7'

YOUTUBE_API_KEY = 'AIzaSyD7VriKrOxv4GXlswm68a4QBy7QItHlDUY'

#Database Stuff
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
