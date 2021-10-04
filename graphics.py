import math

import pygame

WIDTH = 900
HEIGHT = 600
WHITE = (255, 255, 255)
DARKER_WHITE = (120, 120, 120)
BACKGROUND_COLOR = (40, 40, 40)
INCOMPLETE_HANGMAN = (50, 50, 50)
pygame.font.init()
font_normal = pygame.font.SysFont("courier", 16, bold=False)
font_bold = pygame.font.SysFont("courier", 16, bold=True)
font_big_bold = pygame.font.SysFont("courier", 24, bold=True)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galgenraten ihr Gusten")


def redraw_login_menu(host, name, entered_host, entered_name, login_state='OK'):
    win.fill(BACKGROUND_COLOR)

    message = 'Hostname oder IP (leer = localhost): {host}'.format(host=host)
    if not entered_host and not entered_name:
        host = font_bold.render(message, True, WHITE)
    else:
        host = font_normal.render(message, True, WHITE)

    message = 'Name eingeben: {name}'.format(name=name)
    if entered_host and not entered_name:
        name = font_bold.render(message, True, WHITE)
    else:
        name = font_normal.render(message, True, WHITE)

    win.blit(host, (30, 250))
    win.blit(name, (30, 280))

    if entered_host and entered_name:
        fertig = font_bold.render('Verbinde...', True, WHITE)
        win.blit(fertig, (100, 400))

    if login_state == 'ERROR':
        error_text = font_bold.render('Fehler beim Verbinden!', True, WHITE)
        win.blit(error_text, (100, 450))
    if login_state == 'NAME_TAKEN':
        error_text = font_bold.render('Name schon vergeben!', True, WHITE)
        win.blit(error_text, (100, 450))

    pygame.display.update()

    if login_state != 'OK':
        pygame.time.delay(3000)


# Current design can show up to 29 players
def redraw_score_board(player_data, current):
    y_text = 10
    y_line = 29
    for i, (nickname, score) in enumerate(player_data):
        score_str = ''
        if score < 100:
            score_str += ' '
        if score < 10:
            score_str += ' '
        score_str += str(score)

        if i == current:
            nick_text = font_bold.render(nickname, True, WHITE)
            score_text = font_bold.render(score_str, True, WHITE)
        else:
            nick_text = font_normal.render(nickname, True, WHITE)
            score_text = font_normal.render(score_str, True, WHITE)
        win.blit(nick_text, (5, y_text))
        win.blit(score_text, (215, y_text))
        pygame.draw.line(win, WHITE, (0, y_line), (250, y_line), 1)
        y_text += 20
        y_line += 20

    pygame.draw.line(win, DARKER_WHITE, (210, 0), (210, HEIGHT), 1)
    pygame.draw.line(win, WHITE, (250, 0), (250, HEIGHT), 1)


def redraw_hangman(false_attempts):
    def get_color(number):
        if false_attempts >= number:
            return WHITE
        return INCOMPLETE_HANGMAN

    start_x = 400
    start_y = 20
    angle = 30  # In degrees
    len_pole = 350
    len_crossbeam = 170
    distance = 110
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
                         diameter, diameter), 10)

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

    # Remaining attempts
    attempts = font_normal.render('Versuche: ' + str(10 - false_attempts), True, WHITE)
    win.blit(attempts, (start_x + len_crossbeam + 30, start_y + len_noose // 2))


# TODO: Look for better solution of finding appropriate font size
def get_solution_text(solution_formatted, underlines, incomplete_solution, missing_letters, start_x, start_y):
    font_size = 24
    start_font_y = start_y
    while True:
        solution_font = pygame.font.SysFont("courier", font_size, bold=True)
        solution_text = solution_font.render(solution_formatted, True, WHITE)
        incomplete_text = solution_font.render(incomplete_solution, True, WHITE)
        missing_text = solution_font.render(missing_letters, True, DARKER_WHITE)
        start_font_x = int(start_x + (WIDTH - start_x) / 2 - solution_text.get_width() / 2) - 3  # -3 for aesthetics
        if start_x + solution_text.get_width() >= WIDTH:
            font_size -= 1
            start_font_y += 1
        else:
            underlines_text = solution_font.render(underlines, True, WHITE)
            return solution_text, underlines_text, incomplete_text, missing_text, start_font_x, start_font_y


def redraw_enter_solution(solution_text, underlines_text, start_font_x, start_font_y, start_x, start_y):
    win.blit(solution_text, (start_font_x, start_font_y))
    # Move one pixel to the left for better symmetry with letters
    win.blit(underlines_text, (start_font_x - 1, start_font_y))

    message = 'Lösung eingeben (max. 40 Zeichen)'
    text = font_big_bold.render(message, True, WHITE)
    win.blit(text, (start_x + 30, start_y + 60))

    message = 'Erlaubt: A-Z, Leerzeichen, Bindestrich'
    text = font_big_bold.render(message, True, WHITE)
    win.blit(text, (start_x + 30, start_y + 90))


def redraw_chosen_letter(chosen_letter_index, start_x, start_y, game):
    first_line = 'ABCDEFGHIJKLM'
    second_line = 'NOPQRSTUVWXYZ'
    chosen_letter = game.remaining_letters[chosen_letter_index]

    if chosen_letter in first_line:
        choice_x = start_x + 27 + 42 * first_line.find(chosen_letter)
        choice_y = start_y + 60
    else:
        choice_x = start_x + 27 + 42 * second_line.find(chosen_letter)
        choice_y = start_y + 90

    pygame.draw.rect(win, WHITE, (choice_x, choice_y, 21, 25), 2)


def redraw_remaining_letters(game, start_x, start_y):
    line = ''
    for letter in 'ABCDEFGHIJKLM':
        if letter in game.remaining_letters:
            line += letter
        else:
            line += ' '
        line += '  '
    text = font_big_bold.render(line, True, WHITE)
    win.blit(text, (start_x + 30, start_y + 60))

    line = ''
    for letter in 'NOPQRSTUVWXYZ':
        if letter in game.remaining_letters:
            line += letter
        else:
            line += ' '
        line += '  '
    text = font_big_bold.render(line, True, WHITE)
    win.blit(text, (start_x + 30, start_y + 90))


def redraw_guessing_player(chosen_letter_index, start_x, start_y, game):
    redraw_chosen_letter(chosen_letter_index, start_x, start_y, game)
    redraw_remaining_letters(game, start_x, start_y)

    message = 'Du bist dran, du Gust!'
    text = font_big_bold.render(message, True, WHITE)
    win.blit(text, (start_x + 30, start_y + 150))

    message = '(Mit links und rechts wählen und ENTER drücken)'
    text = font_normal.render(message, True, WHITE)
    win.blit(text, (start_x + 25, start_y + 180))


def redraw_hint_special_letters(start_y):
    hint1 = font_normal.render('Ä = AE', True, WHITE)
    win.blit(hint1, (WIDTH - hint1.get_width() - 5, start_y + 140))
    hint2 = font_normal.render('Ü = UE', True, WHITE)
    win.blit(hint2, (WIDTH - hint1.get_width() - 5, start_y + 160))
    hint3 = font_normal.render('Ö = OE', True, WHITE)
    win.blit(hint3, (WIDTH - hint1.get_width() - 5, start_y + 180))
    hint4 = font_normal.render('ß = SS', True, WHITE)
    win.blit(hint4, (WIDTH - hint1.get_width() - 5, start_y + 200))


def redraw_last_move(game):
    if not game.last_letter:
        return
    text = font_normal.render('Geraten: {}'.format(game.last_letter), True, WHITE)
    win.blit(text, (700, 250))
    if game.state == 'win':
        text = font_normal.render('Partie gewonnen', True, WHITE)
        win.blit(text, (700, 270))
    elif game.state == 'lose':
        text = font_normal.render('Partie verloren', True, WHITE)
        win.blit(text, (700, 270))


# Current design allows up to 22 symbols (including spaces and hyphens) with normal size
# Up to 40 symbols with small but still readable font size (should not get smaller)
def redraw_controls(gives_solution, is_solution_giver, my_turn, chosen_letter_index, game):
    start_x = 260
    start_y = 380

    solution_formatted = ''.join([letter.upper() + ' ' for letter in game.solution]).lstrip().rstrip()
    underlines = ''.join(['_' if letter not in [' ', '-', '_'] else ' ' for letter in solution_formatted])
    incomplete_solution = ''.join([letter if letter not in game.remaining_letters + '-' else ' ' for letter in solution_formatted])
    missing_letters = ''.join([letter if letter in game.remaining_letters + '-' else ' ' for letter in solution_formatted])

    # Show what was done in the last move and if game is won or lost
    redraw_last_move(game)

    # Solution progress
    result_solution_text = get_solution_text(solution_formatted, underlines, incomplete_solution, missing_letters, start_x, start_y)
    solution_text, underlines_text, incomplete_text, missing_text, start_font_x, start_font_y = result_solution_text

    pygame.draw.line(win, WHITE, (250, start_y + 40), (WIDTH, start_y + 40), 1)

    # User input
    if not game.entered_solution:  # One player is entering solution
        if gives_solution:  # This player must enter solution
            redraw_enter_solution(solution_text, underlines_text, start_font_x, start_font_y, start_x, start_y)
        else:  # Another player must enter solution
            message = '{} gibt Lösung ein.'.format(game.nicknames[game.solution_giver])
            text = font_big_bold.render(message, True, WHITE)
            win.blit(text, (start_x + 30, start_y + 60))
    else:  # One player is guessing
        win.blit(incomplete_text, (start_font_x, start_font_y))

        # Move one pixel to the left for better symmetry with letters
        win.blit(underlines_text, (start_font_x - 1, start_font_y))

        # Show missing letters if player gave the solution and is not playing alone
        if is_solution_giver and len(game.nicknames) != 1:
            win.blit(missing_text, (start_font_x - 1, start_font_y))

        if my_turn:  # This player's turn to guess
            redraw_guessing_player(chosen_letter_index, start_x, start_y, game)
        else:  # Another player's turn to guess
            redraw_remaining_letters(game, start_x, start_y)
            message = '{} rät.'.format(game.nicknames[game.current_player])
            text = font_big_bold.render(message, True, WHITE)
            win.blit(text, (start_x + 30, start_y + 150))
            pass

    redraw_hint_special_letters(start_y)


def redraw_game_screen(player_data, gives_solution, is_solution_giver, my_turn, chosen_letter_index, game):
    win.fill(BACKGROUND_COLOR)

    redraw_score_board(player_data, game.current_player)
    redraw_hangman(game.failed_attempts)
    redraw_controls(gives_solution, is_solution_giver, my_turn, chosen_letter_index, game)

    pygame.display.update()
