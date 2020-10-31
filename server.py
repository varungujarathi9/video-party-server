# 0 - create room
# 1 - join room
# 2 - play
# 3 - pause
# 4 - play at

# libraries
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import _thread
import time
import datetime
import json
import configparser
from server_utility import get_room_id, send_to_all_clients
# import ServerConfigs

# variables
ServerConfigs = configparser.SafeConfigParser()
ServerConfigs.read('configs.ini')
HOST = ServerConfigs['GeneralSettings']['Host']
PORT = int(ServerConfigs['GeneralSettings']['Port'])
addr = (HOST, PORT)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(addr)
print("socket binded to required address")
serverSocket.listen(10)
client_sockets = []
rooms = {}
channels = {}


def handler():
    global client_sockets
    while True:
        # iterate through all clients
        for client_socket in client_sockets:
            try:
                room_id = None
                sendDataFlag = False
                data = json.loads(client_socket.recv(1024))
                if data['action_id'] == 0:
                    # create room
                    room_id = get_room_id(6)
                    rooms[room_id] = {'members':[data['username']],'video_name': None, 'paused':True, 'playing_at':0, 'total_duration': 0}
                    channels[room_id] = {data['username']:client_socket}
                    client_socket.send(bytes(json.dumps({'join':room_id, 'room':rooms[room_id]}), encoding='utf8'))
                    print("rooms and room id",json.dumps({'join':room_id, 'room':rooms[room_id]}))
                elif data['action_id'] == 1:
                    # join a room
                    if data['room_id'] in rooms:
                        room_id = data['room_id']
                        rooms[room_id]['members'].append(data['username'])
                        
                        #client_socket.send(bytes(json.dumps({room_id:rooms[room_id]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        client_socket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                elif data['action_id'] == 2:
                    # play video
                    if data['room_id'] in rooms:
                        room_id = data['room_id']
                        rooms[room_id]['paused'] = False
                        # client_socket.send(bytes(json.dumps({room_id:rooms[room_id]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        client_socket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                elif data['action_id'] == 3:
                    # pause video
                    if data['room_id'] in rooms:
                        room_id = data['room_id']
                        rooms[room_id]['paused'] = True
                        # client_socket.send(bytes(json.dumps({room_id:rooms[room_id]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        client_socket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                if(sendDataFlag):

                    send_to_all_clients(channels[room_id].values(), json.dumps({room_id:rooms[room_id]}))
                    sendDataFlag = False

            except BlockingIOError:
                pass
            except KeyboardInterrupt:
                for client_socket in client_sockets:
                    client_socket.close()
                client_sockets.clear()
                serverSocket.close()
            except json.decoder.JSONDecodeError:
                client_socket.close()
                client_sockets.remove(client_socket)
                serverSocket.close()
            except (ConnectionResetError, OSError):
                client_socket.close()

# start handler thread which syncs all clients

_thread.start_new_thread(handler, ())
while True:
    try:
        # accpet new client and add client's socket to list
        client_socket, clientAddr = serverSocket.accept()
        if client_socket not in client_sockets:
            client_sockets.append(client_socket)
            client_socket.setblocking(0)
    except (KeyboardInterrupt , OSError):
        print("Closing server socket...")
        serverSocket.close()
        for client_socket in client_sockets:
            client_socket.close()
        client_sockets.clear()
        break