class Hangman:
    def __init__(self):
        self.ready = False
        self.nicknames = []
        self.scores = []
        self.current_player = 0
        self.remaining_letters = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        self.solution = None

    def play(self, player='TODO', move='TODO'):
        if self.ready:
            print('spiel: nein')
        else:
            print('spiel: ja')
        pass

    def reset_game(self):
        self.scores[:] = [0 for _ in self.scores]
        self.remaining_letters = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ']
