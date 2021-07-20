class Hangman:
    def __init__(self):
        self.ready = False
        self.nicknames = []
        self.scores = []
        # self.state ...

    def play(self, player='TODO', move='TODO'):
        print('spiel')
        pass

    def reset_game(self):
        self.scores[:] = [0 for _ in self.scores]
