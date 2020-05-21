from flask import Flask, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, send, emit
from flask_sessionstore import Session
from server import Server

import appauth
import spotipy
import spotipy.util as util
import time
import sys


app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp' #eventually replace with env var
socketio = SocketIO(app)

party = Server()

@socketio.on('start_playback')
def handleSearchClick(msg):
    sp = party.access_token_user_map[session["token_data"]["access_token"]].Spotify
    resp = sp.start_playback(uris=[msg])
    emit('start_playback', msg)

@socketio.on('search')
def handleMessage(msg):
    sp = party.access_token_user_map[session["token_data"]["access_token"]].Spotify
    msgs = sp.search(msg)
    res = ""
    for item in msgs['tracks']['items']:
        artist = ", ".join(list(map(lambda x: x['name'], item['artists'])))
        res += f"""
            <li value="{item["uri"]}">
                <p>{item['name']}</p>
                <p>{artist} {item['album']['name']}</p>
            </li>
            """
    print(res)
    print(party.access_token_user_map)
    emit('search', res)

def usersDisplayHTML(users):
    return  "".join(
        list(map(lambda x: f"""
            <li>
                <p>{x}</p>
            </li>
            """, users)))


@socketio.on('connect')
def handleConnect():
    print("CONNECTED", session['token_data'], party.access_token_user_map)
    print(int(time.time()), session.get('token_expire', -1), sys.maxsize)

    if 'token_expire' not in session or int(time.time()) > session.get('token_expire'):
        print(session.get('token_expire', -1))
        print("REDIRECTING")
        if 'token_data' in session and session['token_data']['access_token'] in party.access_token_user_map:
            del party.access_token_user_map[session['token_data']['access_token']]
        return redirect(appauth.getUser())
    if session['token_data']['access_token'] not in party.access_token_user_map:
        print("adding user")
        party.addUser(session['token_data'])
    print(party.access_token_user_map)
    emit('users', usersDisplayHTML(party.getUserValues('display_name')), BROADCAST=True)

@socketio.on('disconnect')
def handleDisconnect():
    print("DISCONNCTED", party.access_token_user_map, session["token_data"])
    del party.access_token_user_map[session['token_data']['access_token']]
    emit('users', usersDisplayHTML(party.getUserValues('display_name')), BROADCAST=True)
    print("users:", party.access_token_user_map)


@app.route('/')
def index():
    if 'token_data' not in session:
        return redirect(appauth.getUser())
    return render_template('home.html')

@app.route('/callback/')
def login():
    session['token_data'] = appauth.getUserToken(request.args.get('code'))
    if 'token_expire' not in session:
        session['token_expire'] = int(time.time()) + session['token_data']['expires_in']
    print("SESSION TOKEN DATA", session["token_data"], "AAAAAAAA", session["token_expire"])
    return redirect(url_for('home'))

@app.route('/home/', methods=["GET", "POST"])
def home():
    print("HOME", party.access_token_user_map)
    if 'token_data' not in session:
        return redirect(appauth.getUser())
    print(session['token_data'])
    return render_template('home.html')

@app.route('/temp/')
def temp():
    spotify = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(username="temp"))
    print(spotify.me())
    return render_template('home.html')

if __name__ == "__main__":
    socketio.run(app)
