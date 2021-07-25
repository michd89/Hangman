import socket

from utils import send_msg, recv_msg, recv_game


def connect_to_server(host, nick):
    try:
        port = 50000
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        send_msg(client, nick)
        print(f'Antwort vom Server: {recv_msg(client)}')
        return client
    except:
        return None


def send(client, data):
    try:
        send_msg(client, data)
        return recv_game(client)
    except socket.error as e:
        print(e)
