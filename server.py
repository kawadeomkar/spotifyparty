from user import User
from functools import lru_cache

import spotipy


class Server():

    access_token_user_map = {}
    queue = []
    scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing streaming"
    host = ""

    userValues = {
        'display_name': lambda x: x.username['display_name'],
        'access_token': lambda x: x.access_token
    }

    def __init__(self):
        pass

    def addUser(self, token_data, refresh=None):
        host = True if not self.access_token_user_map.keys() else False
        us = User(
            token_data['access_token'],
            token_data['refresh_token'],
            token_data['scope'],
            host = host
        )
        if host:
            self.host = us.username
        self.access_token_user_map[token_data['access_token']] = us
        print("adding token to tmap", self.access_token_user_map)

    @lru_cache(maxsize=None)
    def search(user, query):
        return user.search(query)

    def getUserValues(self, field):
        return list(map(self.userValues[field], self.access_token_user_map.values()))



