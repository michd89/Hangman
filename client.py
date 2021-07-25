import pygame

from graphics import redraw_login_menu, redraw_game_screen
from utils import connect_to_server, send


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
        if event.key == pygame.K_KP_ENTER:
            text_out += '\r'
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

        # Graphics
        if run:
            if not logged_in:
                redraw_login_menu(host, nickname, entered_host, entered_name)
            else:
                # Test
                player_data = [('mICHA', 152),
                               ('Bratwurstkocher', 58),
                               ('tak', 42),
                               ('12345678901234567890', 22),
                               ('Badewannenwinzer', 20),
                               ('Tobsen', 13),
                               ('Dor Ryan', 0),
                               (nickname, 0)
                               ]
                solution = '  der JUNGE mit DeM PeNiS      '
                redraw_game_screen(player_data, solution)


if __name__ == '__main__':
    main()
