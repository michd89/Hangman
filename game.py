class Hangman:
    def __init__(self):
        self.ready = False
        # TODO: Tupel draus machen
        self.nicknames = []
        self.scores = []
        self.current_player = 0
        self.entered_solution = False
        self.failed_attempts = 0
        self.solution_giver = 0
        #self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.remaining_letters = 'ABCDFGHIJKMOPQUVWXYZ'
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

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.nicknames)
        if self.current_player == self.solution_giver:
            self.next_player()

    def new_game(self):
        self.failed_attempts = 0
        self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
