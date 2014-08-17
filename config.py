import os

#statement for enabling the development environment
DEBUG = True

#THIS IS SECRET!!
SECRET_KEY = 'super-secret-password'

#Steam API key
STEAM_API_KEY = os.environ['STEAM_API_KEY']

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']

#Database Stuff
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
