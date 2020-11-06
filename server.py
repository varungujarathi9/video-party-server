# 0 - create room
# 1 - join room
# 2 - play
# 3 - pause
# 4 - play at

# libraries
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, gethostbyaddr
import _thread
import time
import datetime
import json
import configparser
from server_utility import get_room_id, send_to_all_clients
import os
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
room_details = {}
room_sockets = {}

def handler():
    global client_sockets
    while True:
        # iterate through all clients
        for client_socket in client_sockets:
            try:
                room_id = None
                sendDataFlag = False
                data = json.loads(client_socket.recv(1024))
                print(data)
                if data['action_id'] == 0:
                    # check if the client_socket is already present some other room
                    if len(room_details.values()) > 0 and client_socket.getpeername() in [list(y.values()) for y in [x['members'] for x in room_details.values()]][0]:
                        client_socket.send(bytes(json.dumps({'error':"Sorry! Cannot create room, please logout from previous room"}), encoding='utf8'))
                        print("CREATE ROOM VALIDATED",json.dumps({'error':"Sorry! Cannot create room, please logout from previous room"}))
                        # TODO: remove the user from previous room and join in new room
                    else:
                        # create room
                        room_id = get_room_id(6)
                        room_details[room_id] = {'members':{data['username']:client_socket.getpeername()},'video_name': None, 'paused':True, 'playing_at':0, 'total_duration': 0}
                        room_sockets[room_id] = {data['username']:client_socket}
                        
                        client_socket.send(bytes(json.dumps({'created':room_id, 'room_details':room_details[room_id]}), encoding='utf8'))
                        print("CREATE ROOM",json.dumps({'created':room_id, 'room_details':room_details[room_id]}))

                elif data['action_id'] == 1:
                    # join a room
                    print(data)
                    if data['room_id'] not in room_details:
                        client_socket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                    elif data['username'] not in room_sockets[data['room_id']].keys() :
                        client_socket.send(bytes(json.dumps({'error':"User with this "+data['username']+" already exists"}), encoding='utf8'))

                    else:
                        if len(room_details.values()) > 0 and client_socket.getpeername() in [list(y.values()) for y in [x['members'] for x in room_details.values()]][0]:
                            client_socket.send(bytes(json.dumps({'error':"Sorry! Cannot create room, please logout from previous room"}), encoding='utf8'))
                            print("JOIN ROOM VALIDATED",json.dumps({'error':"Sorry! Cannot create room, please logout from previous room"}))
                            # TODO: remove the user from previous room and join in new room
                        else:
                            room_id = data['room_id']
                            room_details[room_id]['members'][data['username']] = client_socket.getpeername()
                            room_sockets[room_id][data['username']] = client_socket

                            sendDataFlag = True
                            print("JOIN ROOM",json.dumps({'join':room_id, 'room_details':room_details[room_id]}))

                elif data['action_id'] == 2:
                    # play video
                    if data['room_id'] in room_details:
                        room_id = data['room_id']
                        room_details[room_id]['paused'] = False

                        sendDataFlag = True
                    else:
                        client_socket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                elif data['action_id'] == 3:
                    # pause video
                    if data['room_id'] in room_details:
                        room_id = data['room_id']
                        room_details[room_id]['paused'] = True
                        # client_socket.send(bytes(json.dumps({room_id:room_details[room_id]}), encoding='utf8'))
                        sendDataFlag = True
                    else:
                        client_socket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                elif data['action_id'] == 4:
                    if data['room_id'] not in room_details:
                        client_socket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))

                    elif data['username'] not in room_details[data['room_id']]['members'].keys() :
                        client_socket.send(bytes(json.dumps({'error':"User with this "+data['username']+" already exists"}), encoding='utf8'))

                    else:
                        # delete user from room_details, room_socket & client_sockets
                        del room_details[data['room_id']]['members'][data['username']]
                        del room_sockets[data['room_id']][data['username']]
                        client_sockets.remove(client_socket)

                        # delete room if there are no members
                        if len(room_details[data['room_id']]['members']) == 0:
                            del room_details[data['room_id']]
                            del room_sockets[data['room_id']]

                    print('EXITED APP:\nRoom Details:',room_details,'\nRoom Sockets',room_sockets, '\nClient Sockets:', client_sockets)        
                elif data['action_id'] == 5:
                    if data['room_id'] not in room_details:
                        client_socket.send(bytes(json.dumps({'error':"Sorry! Room doesn't exist"}), encoding='utf8'))
                    
                    else:
                        read_filename = os.path.basename(data['read_file'])
                        read_fileSize = int(data['read_filesize'])
                        
                        progress = tqdm.tqdm(range(read_fileSize), f"Receiving {read_filename}", unit="B", unit_scale=True, unit_divisor=1024)
                        with open(read_filename, "wb") as f:
                            for _ in progress:
                                # read 1024 bytes from the socket (receive)
                                bytes_read = json.loads(client_socket.recv(4096))
                                if not bytes_read:    
                                    return 
                            
                                f.write(bytes_read)
                                # update the progress bar
                                progress.update(len(bytes_read))

                if(sendDataFlag):
                    send_to_all_clients(room_sockets[room_id].values(), json.dumps({'join':room_id, 'room':room_details[room_id]}))
                    sendDataFlag = False

            except BlockingIOError:
                pass
            except KeyboardInterrupt:
                # for client_socket in client_sockets:
                #     client_socket.close()
                client_sockets.clear()
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except json.decoder.JSONDecodeError:
                # client_socket.close()
                client_sockets.remove(client_socket)

            except (ConnectionResetError, OSError):
                # client_socket.close()
                client_sockets.remove(client_socket)

# start handler thread which syncs all clients

_thread.start_new_thread(handler, ())
while True:
    try:
        # accpet new client and add client's socket to list
        client_socket, client_addr = serverSocket.accept()
        print("Got new client",client_socket)
        if client_socket not in client_sockets:
            client_sockets.append(client_socket)
            client_socket.setblocking(0)
    except KeyboardInterrupt:
        print("Closing server socket...")
        serverSocket.close()
        # for client_socket in client_sockets:
        #     client_socket.close()
        client_sockets.clear()
        break
    except OSError:
        client_sockets.remove(client_socket)