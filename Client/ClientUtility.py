import socket
import json
import time


serverIP = 'localhost'
serverPort = 1397
buf = 1024

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((serverIP, serverPort))

data = {'action_id':0, 'user_id':9}

serverSocket.send(bytes(json.dumps(data), encoding='utf8'))
# print("REPLY: " + str(clientsocket.recv(buf)))
time.sleep(1)
data = {'action_id':1, 'user_id':10, 'room_id':input()}

serverSocket.send(bytes(json.dumps(data), encoding='utf8'))

while True:
    print("REPLY: " + str(serverSocket.recv(buf).decode("utf-8") ))

serverSocket.close()
