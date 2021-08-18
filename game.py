class Hangman:
    def __init__(self):
        self.ready = False
        self.nicknames = []
        self.scores = []
        self.current_player = 0
        self.failed_attempts = '0'
        self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.solution = None

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

    def play(self, player='TODO', move='TODO'):
        if self.ready:
            print('spiel: nein')
        else:
            print('spiel: ja')
        pass

    def reset_game(self):
        self.failed_attempts = 0
        self.scores[:] = [0 for _ in self.scores]
        self.remaining_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
