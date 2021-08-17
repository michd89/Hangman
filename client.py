import pygame

from graphics import redraw_login_menu, redraw_game_screen
from utils import connect_to_server, send


# TODO: Find solution for handling special characters and keys when executed as exe
# exe seems to use encoding for english keyboard layout
def handle_line_typing(event, text_in, max_len=None):
    allowed_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-. '
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
        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            text_out += '\r'
        if not max_len or len(text_out) < max_len:
            if ch in allowed_symbols:
                text_out = text_out + ch
    return text_out


def main():
    client = None
    host = ''
    entered_host = False
    nickname = ''
    entered_name = False
    solution = ''
    entered_solution = False
    must_enter_solution = True  # Test
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
            except Exception as e:
                run = False
                print("Couldn't get game")
                print(e)
                break

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                # Login screen
                if not entered_host:
                    host = handle_line_typing(event, host)
                    if host[-1:] == '\r':
                        host = host[:-1]
                        entered_host = True
                elif not entered_name:
                    # TODO: die zeichenbegrenzung kann man bestimmt in die funktion auslagern
                    nickname = handle_line_typing(event, nickname, 21)
                    if len(nickname) <= 21 and nickname[-1:] == '\r':
                        nickname = nickname[:-1]
                        if not nickname:
                            nickname = 'Namenloser Gust'
                        entered_name = True
                    elif len(nickname) == 21 and nickname[-1:] != '\r':
                        nickname = nickname[:-1]
                # Actual game screen
                else:
                    # Player's turn to enter a solution
                    if must_enter_solution and not entered_solution:
                        solution = handle_line_typing(event, solution, 41)
                        if len(solution) <= 41 and solution[-1:] == '\r':
                            solution = solution[:-1]
                            entered_solution = True
                        elif len(solution) == 41 and solution[-1:] != '\r':
                            solution = solution[:-1]
                        # elif solution[-1:] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ -':
                        #     solution = solution[:-1]
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
                remaining_letters = 'BCDGHIKLMNOQRSUVWY'
                failed_attempts = 4
                redraw_game_screen(player_data, must_enter_solution, solution, remaining_letters, failed_attempts)


if __name__ == '__main__':
    main()
