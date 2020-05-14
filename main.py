from flask import Flask, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, send, emit
from flask_sessionstore import Session
from server import Server

import appauth
import spotipy
import spotipy.util as util


app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp' #eventually replace with env var
socketio = SocketIO(app)

party = Server()

@socketio.on('search')
def handleMessage(msg):
    sp = party.session_id_user_map[request.sid].Spotify
    msgs = sp.search(msg)
    for item in msgs['tracks']['items']:
        song = item['name']
        artist = ", ".join(list(map(lambda x: x['name'], item['artists'])))
        album = item['album']['name']
        uri = item["uri"]
        emit(
            'search',
            f"""
            <li value="{uri}">
                <p>{artist}</p>
                <p>{song}</p>
                <p>{album}</p>
            </li>
            """
        )

@socketio.on('connect')
def handleConnect():
    session["sid"] = request.sid
    print("CONNECTED", request.sid)
    print(session["token_data"])
    party.addUser(session["token_data"], request.sid)
    return redirect(appauth.getUser())

@socketio.on('disconnect')
def handleDisconnect():
    print(party.session_id_user_map[str(request.sid)])
    print(request.sid, session["sid"])
    del party.session_id_user_map[str(request.sid)]


@app.route('/')
def index():
    #print(request.sid)
    resp = appauth.getUser()
    return redirect(resp)

@app.route('/callback/')
def login():
    session["token_data"] = appauth.getUserToken(request.args.get('code'))
    print("SESSION TOKEN DATA", session["token_data"])
    return redirect(url_for('home'))

@app.route('/home/', methods=["GET", "POST"])
def home():
    print(request.args)
    #if request.sid not in party.session_id_user_map.keys():
    #    return redirect(appauth.getUser())
    return render_template('home.html')

if __name__ == "__main__":
    socketio.run(app)
