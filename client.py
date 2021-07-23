import math

import pygame
import socket

from utils import send_msg, recv_msg, recv_game

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
DARKER_WHITE = (120, 120, 120)
BACKGROUND_COLOR = (40, 40, 40)
INCOMPLETE_HANGMAN = (70, 70, 70)
pygame.font.init()
font_normal = pygame.font.SysFont("courier", 16, bold=False)
font_bold = pygame.font.SysFont("courier", 16, bold=True)
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
        return recv_game(client)
    except socket.error as e:
        print(e)


def redraw_login_menu(host, name, entered_host, entered_name, login_error=False):
    win.fill(BACKGROUND_COLOR)

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

    win.blit(host, (30, 250))
    win.blit(name, (30, 280))

    if entered_host and entered_name:
        fertig = font_bold.render('Verbinde...', True, WHITE)
        win.blit(fertig, (100, 400))

    if login_error:
        error_text = font_bold.render('Fehler beim Verbinden!', True, WHITE)
        win.blit(error_text, (100, 450))

    pygame.display.update()

    if login_error:
        pygame.time.delay(3000)


# Current design can show up to 29 players
def redraw_score_board(player_data):
    y_text = 10
    y_line = 29
    for nickname, score in player_data:
        test = font_normal.render(nickname, True, WHITE)
        score_str = ''
        if score < 100:
            score_str += ' '
        if score < 10:
            score_str += ' '
        score_str += str(score)

        test2 = font_normal.render(score_str, True, WHITE)
        win.blit(test, (5, y_text))
        win.blit(test2, (215, y_text))
        pygame.draw.line(win, WHITE, (0, y_line), (250, y_line), 1)
        y_text += 20
        y_line += 20

    pygame.draw.line(win, DARKER_WHITE, (210, 0), (210, HEIGHT), 1)
    pygame.draw.line(win, WHITE, (250, 0), (250, HEIGHT), 1)


def redraw_hangman(false_attempts=0):
    def get_color(number):
        if false_attempts >= number:
            return WHITE
        return INCOMPLETE_HANGMAN


    start_x = 400
    start_y = 20
    angle = 30  # In degrees
    len_pole = 350
    len_crossbeam = 170
    distance = 75
    len_noose = 70
    diameter = 70
    len_torso = 100
    len_arms = 80
    len_legs = 200

    # Right leg
    pygame.draw.line(win, get_color(10),
                     (start_x + len_crossbeam - 3, start_y + len_noose + diameter - 4 + len_torso),
                     (start_x + len_crossbeam - 3 + len_legs * math.cos((270 - angle)),
                      start_y + len_noose + diameter - 4 + len_torso + len_arms * math.sin(270 - angle)),
                     10)

    # Left leg
    pygame.draw.line(win, get_color(9),
                     (start_x + len_crossbeam - 3, start_y + len_noose + diameter - 4 + len_torso),
                     (start_x + len_crossbeam - 3 - len_legs * math.cos((270 - angle)),
                      start_y + len_noose + diameter - 4 + len_torso + len_arms * math.sin(270 - angle)),
                     10)

    # Right arm
    pygame.draw.line(win, get_color(8),
                     (start_x + len_crossbeam - 4, start_y + len_noose + diameter - 4 + int(len_torso * 0.4)),
                     (start_x + len_crossbeam - 4 + len_arms * math.cos((90 + angle)),
                      start_y + len_noose + diameter - 4 + int(len_torso * 0.4) - len_arms * math.sin(90 + angle)),
                     10)

    # Left arm
    pygame.draw.line(win, get_color(7),
                     (start_x + len_crossbeam - 4, start_y + len_noose + diameter - 4 + int(len_torso * 0.4)),
                     (start_x + len_crossbeam - 4 - len_arms * math.cos((90 + angle)),
                      start_y + len_noose + diameter - 4 + int(len_torso * 0.4) - len_arms * math.sin(90 + angle)),
                     10)

    # Torso
    pygame.draw.line(win, get_color(6),
                     (start_x + len_crossbeam - 4, start_y + len_noose + diameter - 4),
                     (start_x + len_crossbeam - 4, start_y + len_noose + diameter + len_torso),
                     10)

    # Head
    pygame.draw.ellipse(win, get_color(5),
                        (start_x + len_crossbeam - diameter // 2 - 3, start_y + len_noose,
                         diameter, diameter), width=10)

    # Noose
    pygame.draw.line(win, get_color(4),
                     (start_x + len_crossbeam - 4, start_y),
                     (start_x + len_crossbeam - 4, start_y + len_noose),
                     10)

    # Brace
    pygame.draw.line(win, get_color(3), (start_x, start_y + distance), (start_x + distance, start_y), 10)

    # Crossbeam
    pygame.draw.line(win, get_color(2), (start_x - 4, start_y + 4), (start_x + len_crossbeam, start_y + 4), 10)

    # Pole
    pygame.draw.line(win, get_color(1), (start_x, start_y), (start_x, start_y + len_pole), 10)


def redraw_game_screen(player_data):
    win.fill(BACKGROUND_COLOR)

    redraw_score_board(player_data)

    # Hangman
    redraw_hangman()

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
    host = ''
    nickname = ''
    entered_host = False
    entered_name = False
    logged_in = False
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        if entered_host and entered_name and not logged_in:
            if not host:
                host = 'localhost'
            client = connect_to_server(host, nickname)
            logged_in = True
            if not client:
                redraw_login_menu(host, nickname, entered_host, entered_name, True)
                pygame.quit()
                break

        # Get current game state before handling user input
        if logged_in:
            try:
                game = send(client, 'get')
                # print(game)
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
                        if not nickname:
                            nickname = 'Namenloser Gust'
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
                # Test
                player_data = [('mICHA', 152), ('Bratwurstkocher', 58), ('tak', 42), ('12345678901234567890', 22), ('Badewannenwinzer', 20), ('Tobsen', 13), ('Dor Ryan', 0)]
                redraw_game_screen(player_data)


if __name__ == '__main__':
    main()