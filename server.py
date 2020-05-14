from user import User

import spotipy


class Server():

    session_id_user_map = {}
    queue = []
    users = []

    def __init__(self):
        self.scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing streaming"


    def addUser(self, token_data, sid):

        us = User(
            token_data["access_token"],
            token_data["refresh_token"],
            token_data["scope"],
            host = True if not self.users else False
        )
        self.session_id_user_map[sid] = us
        self.users.append(us)

