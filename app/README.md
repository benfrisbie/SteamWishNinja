Main API Calls/ Routes
======

0.Page for a game and all the info on it
  ```
  @app.route('/game/<steamAppId>')
  ```
  Where <steamAppId> is the AppID that correlates to a game.  This route should return information about a game such as: the top Twitch.TV stream related to it, a series of YouTube videos that are related to it, and any PcGamer articles that are related.
  This information is not guaranteed and should only be expected for more popular games.  With the most reliable resource being the YouTube view.

1.User profile page
  ```
  @app.route('/user/<nickname>')
  ```
  Where <nickname> is the user's nickname.  This route should return information about the user (their name, profile picture, etc.) and their wishlist.
