import spotipy

class User():

    def __init__(self, access_token, refresh_token, scope, host=False):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.scope = scope
        self.host = host

        self.Spotify = spotipy.Spotify(auth=self.access_token)
        self.username = self.Spotify.current_user()
