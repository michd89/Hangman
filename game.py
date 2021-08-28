class Hangman:
    def __init__(self):
        self.ready = False
        # TODO: Tupel draus machen
        self.nicknames = []
        self.scores = []
        self.current_player = 0
        self.giving_player = 0
        self.entered_solution = False
        self.failed_attempts = 0
        self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.solution = ''

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

    def reset_game(self):
        self.failed_attempts = 0
        self.scores[:] = [0 for _ in self.scores]
        self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
