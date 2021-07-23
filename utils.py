import pickle

ENCODING = 'utf-8'
RECV_SIZE = 4096


def send_msg(sock, msg):
    sock.send(msg.encode(ENCODING))


def recv_msg(sock):
    return sock.recv(RECV_SIZE).decode(ENCODING)


# TODO: Geht das auch normal mit send?
def send_game(sock, game):
    sock.sendall(pickle.dumps(game))


def recv_game(sock):
    return pickle.loads(sock.recv(RECV_SIZE))
