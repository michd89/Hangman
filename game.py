class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.score = 0


class Hangman:
    def __init__(self):
        self.ready = False
        self.players = []
        self.current_player = None
        self.solution_giver = None
        self.entered_solution = False
        self.failed_attempts = 0
        self.state = 'run'
        self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.solution = ''
        self.last_letter = ''

    def set_solution(self, solution):
        self.solution = solution

    def get_player(self, nickname):
        for player in self.players:
            if player.nickname == nickname:
                return player
        return None

    # TODO: Zufällig mit insert einfügen
    def add_player(self, nickname):
        if self.get_player(nickname):
            return False
        new_player = Player(nickname)
        if not self.players:
            self.current_player = self.solution_giver = new_player
        self.players.append(new_player)
        return True

    def delete_player(self, nickname):
        player = self.get_player(nickname)
        if player:
            del player
            self.next_player()
            return True
        return False

    def start_guessing(self):
        self.entered_solution = True
        self.next_player()

    def evaluate_match(self):
        if self.failed_attempts == 10:
            self.state = 'lose'
        # Check if there are still remaining letters not chosen yet
        elif not set(self.solution).intersection(set(self.remaining_letters)):
            self.state = 'win'
        else:
            self.state = 'run'
        return

    def guess_letter(self, letter):
        if letter in self.remaining_letters and letter in self.solution:
            self.current_player.score += 1
        else:
            self.failed_attempts += 1
        self.remaining_letters = self.remaining_letters.replace(letter, '')
        self.last_letter = letter
        self.evaluate_match()
        if self.state == 'lose':
            self.solution_giver.score += 3
            self.new_game()
        elif self.state == 'win':
            self.new_game()
        else:
            self.next_player()

    def next_player(self):
        # Play the game in some kind of singleplayer/local mode
        if len(self.players) == 1:
            return self.players[0]

        index = self.players.index(self.current_player)
        if index == len(self.players) - 1:
            self.current_player = self.players[0]
        else:
            self.current_player = self.players[index + 1]
        if self.current_player == self.solution_giver:
            self.next_player()
        return self.current_player

    def new_game(self):
        self.entered_solution = False
        self.solution = ''
        self.failed_attempts = 0
        self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.solution_giver = self.next_player()
