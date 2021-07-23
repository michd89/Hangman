import pickle

import pygame
import socket

from utils import send_msg, recv_msg, RECV_SIZE

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (40, 40, 40)
pygame.font.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galgenraten ihr Gusten")


def connect_to_server(host, nick):
    try:
        port = 50000
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        send_msg(client, nick)
        print(f'Antwort vom Server: {recv_msg(client)}')
        return client
    except:
        pass


def send(client, data):
    try:
        send_msg(client, data)
        return pickle.loads(client.recv(RECV_SIZE))
    except socket.error as e:
        print(e)


def redraw_login_menu(host, name, entered_host, entered_name, login_error=False):
    win.fill(BACKGROUND_COLOR)

    font_normal = pygame.font.SysFont("courier", 20, bold=False)
    font_bold = pygame.font.SysFont("courier", 20, bold=True)

    message = f'Hostname oder IP (leer = localhost): {host}'
    if not entered_host and not entered_name:
        host = font_bold.render(message, True, WHITE)
    else:
        host = font_normal.render(message, True, WHITE)

    message = f'Name eingeben: {name}'
    if entered_host and not entered_name:
        name = font_bold.render(message, True, WHITE)
    else:
        name = font_normal.render(message, True, WHITE)

    win.blit(host, (100, 250))
    win.blit(name, (100, 280))

    if entered_host and entered_name:
        fertig = font_bold.render('Verbinde...', True, WHITE)
        win.blit(fertig, (100, 400))

    if login_error:
        error_text = font_bold.render('Fehler beim Verbinden!', True, WHITE)
        win.blit(error_text, (100, 450))

    pygame.display.update()

    if login_error:
        pygame.time.delay(3000)


def redraw_game_screen():
    win.fill(BACKGROUND_COLOR)

    # ...

    pygame.display.update()


def handle_text_typing(event, text_in, max_len=None):
    text_out = text_in
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_BACKSPACE]:
        text_out = text_out[:-1]
    else:
        try:
            ch = chr(event.key)
        except:
            ch = ''
        if pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT]:
            ch = ch.upper()
        if not max_len or len(text_out) < max_len:
            text_out = text_out + ch
    return text_out


def main():
    client = None
    nickname = None
    run = True
    entered_host = False
    entered_name = False
    host = ''
    nickname = ''
    logged_in = False
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        if entered_host and entered_name and not logged_in:
            try:
                if not host:
                    host = 'localhost'
                client = connect_to_server(host, nickname)
                logged_in = True
            except:
                print('Fehler beim Login')
                redraw_login_menu(host, nickname, entered_host, entered_name, True)
                pygame.quit()
                run = False
                break

        # Get current game state before handling user input
        if logged_in:
            try:
                game = send(client, 'get')
                print(game)
            except:
                run = False
                print("Couldn't get game")
                break

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                # Login screen
                if not entered_host:
                    host = handle_text_typing(event, host)
                    if host[-1:] == '\r':
                        host = host[:-1]
                        entered_host = True
                elif not entered_name:
                    # TODO: die zeichenbegrenzung kann man bestimmt in die funktion auslagern
                    nickname = handle_text_typing(event, nickname, 21)
                    if len(nickname) <= 21 and nickname[-1:] == '\r':
                        nickname = nickname[:-1]
                        entered_name = True
                    elif len(nickname) == 21 and nickname[-1:] != '\r':
                        nickname = nickname[:-1]
                # Actual game screen
                else:
                    pass

        # Game mechanics
        if run:
            if not logged_in:
                redraw_login_menu(host, nickname, entered_host, entered_name)
            else:
                redraw_game_screen()


if __name__ == '__main__':
    main()