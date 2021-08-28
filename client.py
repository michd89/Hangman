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
    logged_in = False
    solution = ''
    game = None  # For suppressing warning
    gives_solution = False  # For suppressing warning
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        if entered_host and entered_name and not logged_in:
            client = connect_to_server(host, nickname)
            logged_in = True
            if client == 'NOPE':
                redraw_login_menu(host, nickname, entered_host, entered_name, 'NAME_TAKEN')
                pygame.quit()
                break
            if not client:
                redraw_login_menu(host, nickname, entered_host, entered_name, 'ERROR')
                pygame.quit()
                break

        # Get current game state before handling user input
        if logged_in:
            try:
                game = send(client, 'get')
                gives_solution = nickname == game.nicknames[game.current_player] and not game.entered_solution
                # print(game)
            except Exception as e:
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
                        if not host:
                            host = 'localhost'
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
                    if gives_solution:
                        solution = handle_line_typing(event, solution, 41)
                        if solution == ' ':  # No leading space
                            solution = ''
                        elif len(solution) >= 2 and solution[-2:] == '  ':  # No multiple trailing spaces
                            solution = solution[:-1]
                        elif len(solution) <= 41 and solution[-1:] == '\r':
                            solution = solution[:-1]
                            if solution:  # No empty solution
                                send(client, 'enter')
                        elif len(solution) == 41 and solution[-1:] != '\r':
                            solution = solution[:-1]
                        elif solution[-1:] not in 'abcdefghijklmnopqrstuvwxyz -':
                            solution = solution[:-1]
                        send(client, 'solution ' + solution.upper())
        # Graphics
        if run:
            if not logged_in:
                redraw_login_menu(host, nickname, entered_host, entered_name)
            else:
                # TODO: Sort
                # https://stackoverflow.com/questions/8459231/sort-tuples-based-on-second-parameter
                player_data = list(zip(game.nicknames, game.scores))
                redraw_game_screen(player_data, gives_solution, game)


if __name__ == '__main__':
    main()
