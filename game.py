class Hangman:
    def __init__(self):
        self.ready = False
        self.nicknames = []
        self.scores = []
        self.current_player = 0
        self.solution = None

    def play(self, player='TODO', move='TODO'):
        print('spiel')
        pass

    def reset_game(self):
        self.scores[:] = [0 for _ in self.scores]
