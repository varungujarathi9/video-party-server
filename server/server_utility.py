import random
import string
import json

def get_room_id(length):
    letters_and_digits = string.ascii_uppercase + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    print("Random alphanumeric String is:", result_str)
    return result_str

def send_to_all_clients(clientSockets, stringData):
    for clientSocket in clientSockets:
        clientSocket.send(bytes(stringData, encoding='utf8'))