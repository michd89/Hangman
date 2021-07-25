import pickle
import socket

ENCODING = 'utf-8'
RECV_SIZE = 4096


def send_msg(sock, msg):
    sock.send(msg.encode(ENCODING))


def recv_msg(sock):
    return sock.recv(RECV_SIZE).decode(ENCODING)


# TODO: Geht das auch mit send?
def send_game(sock, game):
    sock.sendall(pickle.dumps(game))


def recv_game(sock):
    return pickle.loads(sock.recv(RECV_SIZE))


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


# Send message to server and receive game
def send(client, data):
    try:
        send_msg(client, data)
        return recv_game(client)
    except socket.error as e:
        print(e)
