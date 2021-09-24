import socket
import threading

from game import Hangman
from utils import recv_msg, send_msg, send_game

game = Hangman()


# Sub thread: Handles messages from certain client
def handling_client_thread_function(client):
    nickname = recv_msg(client)
    if game.add_player(nickname):
        print('{nickname} ist dem Spiel beigetreten'.format(nickname=nickname))
        send_msg(client, 'OK')
    else:
        print('{nickname} gibts schon'.format(nickname=nickname))
        send_msg(client, 'NOPE')
        client.close()
        return

    while True:
        try:
            message = recv_msg(client)

            if not message:  # Player left game
                break
            # if message.startswith('reset'):
            #     game.reset_game()
            elif message.startswith('solution'):
                game.solution = message[len('solution')+1:]  # TODO: In Klassenmethode auslagern
            elif message.startswith('enter'):
                game.start_guessing()
            elif message.startswith('guess'):
                game.guess_letter(message[len('guess')+1:])

            send_game(client, game)
        except Exception as exc:
            # Remove and close client
            client.close()
            game.delete_player(nickname)
            print('{nickname} hat das Spiel verlassen (exc)'.format(nickname=nickname))
            print(exc)
            break
    game.delete_player(nickname)
    print('{nickname} hat das Spiel verlassen (normal)'.format(nickname=nickname))


# Main thread: Receiving / Listening function
def receive():
    host = '0.0.0.0'
    port = 50000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print('Server horcht auf {host}:{port} ...'.format(host=host, port=port))

    while True:
        # Accept connection
        client, address = server.accept()
        print("Verbunden mit {}".format(str(address)))

        # Start handling thread for client
        thread = threading.Thread(target=handling_client_thread_function, args=([client]))
        thread.start()


if __name__ == '__main__':
    receive()
