
from flask import Flask,request,redirect,current_app
from flask_socketio import SocketIO,emit
import json

#instantiate
app = Flask(__name__)
app.config['SECRET_KEY'] = 'videoparty100'

#wrapping flask instance with the socketio wrapper
socketIo = SocketIO(app,cors_allowed_origins="*")

@socketIo.on('connect')
def client_connect():
    emit("connected",{'msg':"welcome to videoparty"})
    print("client connectecd")

@socketIo.on('message')
def handleMessage(data):
    print("username receiving")
    print(data)
    emit('outgoingdata',data)
    return None


@socketIo.on('disconnect')
def client_disconnect():
    print("client disconnected")





if __name__ == '__main__':
    #automatic reloads again when made some changes
    app.debug=True
    socketIo.run(app)
