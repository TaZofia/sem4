import random
class Board:

    def __init__(self, size):
        self.size = size        # size - number of elements in row/column
        self.board = []
        self.generate_perm()


    def generate_perm(self):
        for i in range((self.size ** 2) - 1):
            self.board.append(i + 1)

        random.shuffle(self.board)
        self.board.append(0)

    def print_board(self):
        padding = len(str(len(self.board) - 1))
        for i in range(self.size ** 2):
            print(str(self.board[i]).zfill(padding), end=" ")
            if (i + 1) % self.size == 0:
                print()

    @property
    def get_board(self):
        return self.board


    def valid_moves(self):

        index_of_empty = self.board.index(0)

        left = index_of_empty - 1
        right = index_of_empty + 1
        up = index_of_empty - self.size
        down = index_of_empty + self.size

        moves = []

        if up >= 0:
            moves.append(up)
        if right % self.size != 0:
            moves.append(right)
        if down <= self.size ** 2 - 1:
            moves.append(down)
        if left % self.size != self.size - 1:
            moves.append(left)

        print(moves)


board = Board(4)
board.print_board()

board.valid_moves()

