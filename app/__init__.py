
# ****************************** __init__.py ******************************
# This is called right after the application is started, run.py is ran. As
# the name implies necassary initializations should be performed here.
# *************************************************************************

from flask import Flask

#Creates the application object of type Flask
app = Flask(__name__)
from app import views
