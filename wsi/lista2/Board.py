import random
class Board:

    def __init__(self, size):
        self.size = size
        self.board = []


    def generate_perm(self):

        for i in range(self.size - 1):
            self.board.append(i + 1)

        random.shuffle(self.board)
        self.board.append(0)


board1 = Board(20)
board1.generate_perm()

print(board1.board)