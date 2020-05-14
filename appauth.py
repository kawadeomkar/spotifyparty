from auth import getAuth, refreshAuth, getToken

CLIENT_ID = "c1b3feade2424df8aac21d2280aa9304"
CLIENT_SECRET = "b8de723d1377470c8838c39e68c18894"

PORT = "5000"
CALLBACK_URL = "http://localhost"

SCOPE = "streaming"
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
    return TOKEN_DATA

def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA

