
# ****************************** youtube_requests.py *****************************
# Holds all of our requests that will be sent to the youtube api.
# *******************************************************************************

import requests, json
from config import YOUTUBE_API_KEY

# Get a list of videoIds pertaining to the game being searched
def search_videos(game):
    params = {
        'key': YOUTUBE_API_KEY,
        'part': 'snippet',
        'maxResults': 3,
        'order': 'relevance',
        'q': game.name +'video game',
        'type': 'video',
        'videoEmbeddable': True
    }

    url = 'https://www.googleapis.com/youtube/v3/search'
    rv = requests.get(url, params=params).json()

    video_ids = []
    if(rv['pageInfo']['totalResults'] != 0):
    	for video in rv['items']:
    		video_ids.append(video['id']['videoId'])

    return video_ids