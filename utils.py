ENCODING = 'utf-8'
RECV_SIZE = 4096


def send_msg(sock, msg):
    sock.send(msg.encode(ENCODING))


def recv_msg(sock):
    return sock.recv(RECV_SIZE).decode(ENCODING)
