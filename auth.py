import base64, json, requests
import logging

AUTH_URL = 'https://accounts.spotify.com/authorize/?'
AUTH_TOKEN = 'https://accounts.spotify.com/api/token/'
RESPONSE_TYPE = 'code'
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''

def getAuth(client_id, redirect_uri, scope):
    data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(AUTH_URL, client_id, redirect_uri, scope) 
    return data

def getToken(code, client_id, client_secret, redirect_uri):
    body = {
        "grant_type": 'authorization_code',
        "code" : code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }

    encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode('utf-8')).decode('utf-8')
    headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(encoded)} 

    post = requests.post(AUTH_TOKEN, params=body, headers=headers)
    if post.status_code != 200:
        print(post.status_code, post.text)
        if post.status_code == 400:
            # TODO: handle invalid auth code error
            logging.error("400: AUTH TOKEN EXPIRED")
            raise Exception
        raise Exception
    return json.loads(post.text)

def handleToken(response):
    auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
    REFRESH_TOKEN = response["refresh_token"]
    return [response["access_token"], auth_head, response["scope"], response["expires_in"]]

def refreshAuth():
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : REFRESH_TOKEN
    }

    post_refresh = requests.post(AUTH_TOKEN, data=body, headers=HEADER)
    p_back = json.dumps(post_refresh.text)
    return handleToken(p_back)

