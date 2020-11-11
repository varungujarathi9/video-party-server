import flask
from flask import *
from flask_socketio import SocketIo,emit

app = Flask(__name__)

socketio = SocketIO(app)



@socketio.on('my event')
def test_message(message):
    print("checking msg",message)
    emit('my response',message)


