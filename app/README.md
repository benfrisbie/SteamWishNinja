Main API Calls/ Routes
======

0.Page for a game and all the info on it
  @app.route('/game/<steamAppId>')
  Where <steamAppId> is the AppID that correlates to a game.  

1.User profile page
  @app.route('/user/<nickname>')
  Where <nickname> is the user's nickname.  This route should return information about the user (their name, profile picture, etc.) and their wishlist.
  
