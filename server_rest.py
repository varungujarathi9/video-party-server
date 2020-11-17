
from flask import Flask,request,redirect,current_app
from flask_socketio import SocketIO,emit

app = Flask(__name__)

socketio = SocketIO(app,cors_allowed_origins="*")


# with app.app_context():
#     # within this block, current_app points to app.
#     print(current_app.name)

WELCOME_MSG=[{"welcome_msg":"Welcome to local video player"}]


@socketio.on('connect')
def client_connect():
    print("client connectecd")
    emit('MESSAGE',WELCOME_MSG) 

@socketio.on('disconnect')
def client_disconnect():
    print("client disconnected")

# @socketio.on("message")
# def test_message(username):
#     print("checking username",username)
#     emit("username",username)
#     return none
    
if __name__ == '__main__':
    app.debug=True
    socketio.run(app)
