
# ****************************** __init__.py ******************************
# This is called right after the application is started, run.py is ran. As
# the name implies necassary initializations should be performed here.
# *************************************************************************

from flask import Flask, redirect, session, json, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from config import SECRET_KEY

#Creates the application object of type Flask
app = Flask(__name__)
app.secret_key = SECRET_KEY
oid = OpenID(app)
from app import views
