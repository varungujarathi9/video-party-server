
# from flask import Flask,request,redirect,current_app, jsonify
# from flask_socketio import SocketIO, emit, join_room, leave_room
# import json
# import string
# import random
# import datetime
# import pytz
# import json

# #instantiate
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'videoparty100'

# #wrapping flask instance with the socketio wrapper
# socketIo = SocketIO(app,cors_allowed_origins="*")

# timezone = pytz.timezone('Asia/Kolkata')

# rooms_details = {}
 
# def get_room_id(length):
#     letters_and_digits = string.ascii_uppercase + string.digits
#     result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
#     print("Random alphanumeric String is:", result_str)
#     return result_str

# @socketIo.on('create-room')
# def create_room(data):
#     global rooms_details
#     room_id = get_room_id(6)
#     rooms_details[room_id] = {'members':[data['username']],'created_at':datetime.datetime.now(tz=timezone).strftime('%x @ %X'),  'video_name': None, 'paused':True, 'playing_at':0, 'total_duration': 0}
#     join_room(room_id)
#     emit('room-created', {'room-id':room_id, 'room-details':rooms_details[room_id]})

# @socketIo.on('join-room')
# def joinroom(data):
#     global rooms_details
#     rooms_details[data['roomID']]['members'].append(data['username'])
#     join_room(data['roomID'])
#     emit('room-joined', {'room-id':data['roomID'], 'room-details':rooms_details[data['roomID']]})
#     emit('update-joinee', rooms_details[data['roomID']], broadcast=True, include_self=False,room=data['roomID'])

# @socketIo.on('start-video')
# def start_video(room_id):
#     emit('video-started', broadcast=True, include_self=True, room=room_id['room_id'])
    
# @socketIo.on('video-update')
# def video_update(data):
#     print('playing: ',data['pauseDetails']['playing'])
#     print('progressTime',data['pauseDetails']['progressTime'])
#     emit('updated-video',data, broadcast=True, include_self=False,room=data['pauseDetails']['roomID'] )

# @socketIo.on('remove-member')
# def remove_member(data):
#     global rooms_details
#     rooms_details[data['roomID']]['members'].remove(data['username'])    
#     leave_room(data['roomID'])
#     print(data)
#     emit('left_room',rooms_details[data['roomID']])
#     emit('update-joinee', rooms_details[data['roomID']], broadcast=True, include_self=False,room=data['roomID'])


# @socketIo.on('remove-all-member')
# def remove_all_members(data):
#     global rooms_details
#     rooms_details[data['roomID']]['members'].clear()
#     emit('all_left',rooms_details[data['roomID']],broadcast=True, include_self=True, room=data['roomID'])
#     leave_room(data['roomID'])

# if __name__ == '__main__':
#     #automatic reloads again when made some changes
#     app.debug=True
#     # use this while running in gcsp server
#     socketIo.run(app, host='0.0.0.0', port=5000)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()