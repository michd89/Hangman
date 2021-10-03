class Hangman:
    def __init__(self):
        self.ready = False
        # TODO: Tupel draus machen
        # Oder gar eine Spielerklasse mit Punkten, Status etc.?
        self.nicknames = []
        self.scores = []
        self.current_player = 0
        self.entered_solution = False
        self.failed_attempts = 0
        self.solution_giver = 0
        self.state = 'run'
        self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.solution = ''

    # TODO: Zufällig mit insert einfügen
    def add_player(self, nickname):
        if nickname in self.nicknames:
            return False
        self.nicknames.append(nickname)
        self.scores.append(0)
        return True

    def delete_player(self, nickname):
        index = self.nicknames.index(nickname)
        del(self.scores[index])
        del(self.nicknames[index])
        self.next_player()

    # TODO: Am besten hier immer neu Reihenfolge mischen
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
            self.scores[self.current_player] += 1
        else:
            self.failed_attempts += 1
        self.remaining_letters = self.remaining_letters.replace(letter, '')
        self.evaluate_match()
        if self.state == 'lose':
            self.scores[self.solution_giver] += 3
            self.new_game()
        elif self.state == 'win':
            self.new_game()
        else:
            self.next_player()

    def next_player(self):
        # Play the game in some kind of singleplayer/local mode
        if len(self.nicknames) == 1:
            return 0

        self.current_player = (self.current_player + 1) % len(self.nicknames)
        if self.current_player == self.solution_giver:
            self.next_player()
        return self.current_player

    def new_game(self):
        self.entered_solution = False
        self.solution = ''
        self.failed_attempts = 0
        self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.solution_giver = self.next_player()
