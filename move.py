class Move:
    def __init__(self, before, after, move):
        self.before = before
        self.after  = after
        self.move   = move

        if move == 'place':
            self.move = 1
        elif move == 'remove':
            self.move = 2
        else:
            self.move = 0