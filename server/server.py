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
clientSockets = []
rooms = {}
channels = {}


def handler():
    global clientSockets
    while True:
        # iterate through all clients
        for clientSocket in clientSockets:
            try:
                roomID = None
                sendDataFlag = False
                data = json.loads(clientSocket.recv(1024))
                if data['action_id'] == 0:
                    # create room
                    roomID = get_room_id(6)
                    rooms[roomID] = {'members':[data['username']], 'video_name': None, 'paused':True, 'playing_at':0, 'total_duration': 0}
                    channels[roomID] = {data['username']:clientSocket}
                    clientSocket.send(bytes(json.dumps({'join':roomID, 'room':rooms[roomID]}), encoding='utf8'))

                elif data['action_id'] == 1:
                    # join a room
                    if data['room_id'] in rooms:
                        roomID = data['room_id']
                        rooms[roomID]['members'].append(data['username'])
                        # clientSocket.send(bytes(json.dumps({roomID:rooms[roomID]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        clientSocket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                elif data['action_id'] == 2:
                    # play video
                    if data['room_id'] in rooms:
                        roomID = data['room_id']
                        rooms[roomID]['paused'] = False
                        # clientSocket.send(bytes(json.dumps({roomID:rooms[roomID]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        clientSocket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                elif data['action_id'] == 3:
                    # pause video
                    if data['room_id'] in rooms:
                        roomID = data['room_id']
                        rooms[roomID]['paused'] = True
                        # clientSocket.send(bytes(json.dumps({roomID:rooms[roomID]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        clientSocket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                if(sendDataFlag):
                    
                    send_to_all_clients(rooms[roomID]['members'], json.dumps({roomID:rooms[roomID]}))
                    sendDataFlag = False

            except BlockingIOError:
                pass
            except KeyboardInterrupt:
                for clientSocket in clientSockets:
                    clientSocket.close()
                clientSockets.clear()
                serverSocket.close()
            except json.decoder.JSONDecodeError:
                clientSocket.close()
                clientSockets.remove(clientSocket)
                serverSocket.close()
            except ConnectionResetError:
                clientSocket.close()

# start handler thread which syncs all clients

_thread.start_new_thread(handler, ())
while True:
    try:
        # accpet new client and add client's socket to list
        clientSocket, clientAddr = serverSocket.accept()
        if clientSocket not in clientSockets:
            clientSockets.append(clientSocket)
            clientSocket.setblocking(0)
    except (KeyboardInterrupt , OSError):
        print("Closing server socket...")
        serverSocket.close()
        for clientSocket in clientSockets:
            clientSocket.close()
        clientSockets.clear()
        break