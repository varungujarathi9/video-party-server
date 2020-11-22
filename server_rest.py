
from flask import Flask,request,redirect,current_app, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import string
import random
import datetime
import pytz
import json

#instantiate 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'videoparty100'

#wrapping flask instance with the socketio wrapper
socketIo = SocketIO(app,cors_allowed_origins="*")

timezone = pytz.timezone('Asia/Kolkata')

rooms_details = {}
 
def get_room_id(length):
    letters_and_digits = string.ascii_uppercase + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    print("Random alphanumeric String is:", result_str)
    return result_str

@socketIo.on('create-room')
def create_room(data):
    room_id = get_room_id(6)
    rooms_details[room_id] = {'members':[data['username']],'created_at':datetime.datetime.now(tz=timezone).strftime('%x @ %X'),  'video_name': None, 'paused':True, 'playing_at':0, 'total_duration': 0}
    join_room(room_id)
    emit('room-created', {'room-id':room_id, 'room-details':rooms_details[room_id]})

@socketIo.on('message')
def handleMessage(data):   
    print("username receiving")
    print("data is:",data['data'])
    # room_Id = get_room_id()
    # room_details={'room_id':room_Id,'data':data['data']}
    username_details={'data':data['data']}
    print("-----------------------------------")
    emit('outgoingdata',username_details)
    return None

#create room roomid function
@socketIo.on('my_roomId')
def handleRoomId():
    room_Id = get_room_id()
    ROOM_ID_ARRAY.append(room_Id)
    print('all room ids ',ROOM_ID_ARRAY)
    room_details={'roomid':room_Id}
    print("room details is:",room_details)
    print("------------------------")
    emit('emitRoomId',room_details)
    return None

#join room  roomid function
@socketIo.on('room_id')
def receiveRoomId(joinRoom):
    username=joinRoom['joinRoom']['userName']
    joinIdValid = joinRoom['joinRoom']['sendRoomId']
    if(joinIdValid in ROOM_ID_ARRAY):
        join_room(joinIdValid)
        memberslist={'membersName':username}
        emit('newJoinee', memberslist,room=joinIdValid, broadcast=True)
        print('receiving joinees username',username)
    else:
        print("such room id doesnt exist")

    

# @socketIo.on('my_joiningId')
# def receiveJoinId(sendRoomId):
#     print('join')





if __name__ == '__main__':
    #automatic reloads again when made some changes
    app.debug=True
    socketIo.run(app, host="0.0.0.0", port=5000)
