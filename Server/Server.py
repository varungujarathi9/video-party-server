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
from ServerUtility import getRandomAlphanumericString, sendToAllClients
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
serverSocket.listen(10)
clientSockets = []
rooms = {}
channels = {}


def handler():
    global clientSockets
    sendDataFlag = False
    while True:
        # iterate through all clients
        for clientSocket in clientSockets:
            try:
                roomID = None
                data = json.loads(clientSocket.recv(1024))
                if data['action_id'] == 0:
                    # create room
                    roomID = getRandomAlphanumericString(6)
                    rooms[roomID] = {'members':[data['user_id']], 'video_name': None, 'paused':True, 'playing_at':0, 'total_duration': 0}
                    channels[roomID] = {data['user_id']:clientSocket}
                    sendDataFlag = True
                    # clientSocket.send(bytes(json.dumps({roomID:rooms[roomID]}), encoding='utf8'))
                elif data['action_id'] == 1:
                    # join a room
                    if data['room_id'] in rooms:
                        roomID = data['room_id']
                        rooms[roomID]['members'].append(data['user_id'])
                        clientSocket.send(bytes(json.dumps({roomID:rooms[roomID]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        clientSocket.send(bytes("Sorry! Room doesn't exist"))
                elif data['action_id'] == 2:
                    # play video
                    if data['room_id'] in rooms:
                        roomID = data['room_id']
                        rooms[roomID]['paused'] = False
                        # clientSocket.send(bytes(json.dumps({roomID:rooms[roomID]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        clientSocket.send(bytes("Sorry! Room doesn't exist"))

                elif data['action_id'] == 3:
                    # play video
                    if data['room_id'] in rooms:
                        roomID = data['room_id']
                        rooms[roomID]['paused'] = True
                        # clientSocket.send(bytes(json.dumps({roomID:rooms[roomID]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        clientSocket.send(bytes("Sorry! Room doesn't exist"))

                if(sendDataFlag):
                    sendToAllClients(clientSockets, json.dumps({roomID:rooms[roomID]}))
                    sendDataFlag = False
                    
            except BlockingIOError:
                pass
            except KeyboardInterrupt:
                for clientSocket in clientSockets:
                    clientSocket.close()
                clientSockets.clear()
            except json.decoder.JSONDecodeError:
                clientSocket.close()
                clientSockets.remove(clientSocket)
    # TODO: close sockets after room closing

# start handler thread which syncs all clients

# _thread.start_new_thread(handler, ())
while True:
    try:
        # accpet new client and add client's socket to list
        clientSocket, clientAddr = serverSocket.accept()
        clientSockets.append(clientSocket)
        clientSocket.setblocking(0)
    except (KeyboardInterrupt , OSError):
        print("Closing server socket...")
        serverSocket.close()
        for clientSocket in clientSockets:
            clientSocket.close()
        clientSockets.clear()
        break