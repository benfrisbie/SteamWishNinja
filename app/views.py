
# ****************************** views.py *********************************
# Holds all the handlers that will respond to requests from the browser.
# Each python function in here will map to 1 or more request URLs.
# *************************************************************************

from app import app

# The first page/home that will be displayed first
@app.route('/')
def index():
    return "Hello, World!"
