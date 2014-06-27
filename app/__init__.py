
# ****************************** __init__.py ******************************
# This is called right after the application is started, run.py is ran. As
# the name implies necassary initializations should be performed here.
# *************************************************************************

import os
from flask import Flask, redirect, session, json, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from config import SECRET_KEY, basedir

#Creates the application object of type Flask
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config.from_object('config')
db = SQLAlchemy(app, os.path.join(basedir, 'app/db_repository/tmp'))
oid = OpenID(app)
from app import views, models
