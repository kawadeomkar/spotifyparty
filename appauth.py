from auth import getAuth, refreshAuth, getToken
import os

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_REDIRECT_URL = os.environ["SPOTIPY_REDIRECT_URL"]
PORT = "5000"
TOKEN_DATA = []
# TODO: move scope from server
SCOPE = "streaming"

def getUser():
    return getAuth(SPOTIPY_CLIENT_ID, "{}:{}/callback/".format(SPOTIPY_REDIRECT_URI, PORT), SCOPE)

def getUserToken(code):
    TOKEN_DATA = getToken(code, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, "{}:{}/callback/".format(SPOTIPY_REDIRECT_URI, PORT))
    return TOKEN_DATA

def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA

