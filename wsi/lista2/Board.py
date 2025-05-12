import random
import hashlib

from pandas.core.util.hashing import hash_array


class Board:

    def __init__(self, size, parent = None):
        self.size = size        # size - number of elements in row/column
        self.board = []
        self._generate_perm()
        self.h = 0
        self.g = 0
        self.f = self.g + self.h
        self.move_that_was_made = None
        self.parent = parent
        self.Id = None

    @property
    def get_board(self):
        return self.board

    '''
    @property
    def board(self):
    return board

    MyBoard.get_board
    MyBoard.board
    '''
    def _generate_perm(self):
        for i in range((self.size ** 2) - 1):
            self.board.append(i + 1)

        random.shuffle(self.board)
        self.board.append(0)

    def hash_board(self):
        array_str = str(tuple(self.board))
        hash_array = hashlib.md5(array_str.encode())

        self.Id = hash_array.hexdigest()

    def _number_of_inversions(self):
        def merge_sort(arr):
            if len(arr) <= 1:
                return arr, 0

            mid = len(arr) // 2
            left, inv_left = merge_sort(arr[:mid])
            right, inv_right = merge_sort(arr[mid:])
            merged, inv_split = merge_and_count(left, right)

            return merged, inv_left + inv_right + inv_split

        def merge_and_count(left, right):
            merged = []
            i = j = inv_count = 0

            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    inv_count += len(left) - i  # other left elements are inversions
                    j += 1

            merged += left[i:]
            merged += right[j:]
            return merged, inv_count

        # skip 0
        filtered_board = [num for num in self.board if num != 0]
        _, inv_count = merge_sort(filtered_board)
        return inv_count


    def _get_blank_row_number(self):
        index_of_blank = self.board.index(0)
        row = index_of_blank % self.size
        return self.size - row              # because we numerate rows from 1 from the bottom


    def can_be_solved(self):
        if (self._number_of_inversions() + self._get_blank_row_number()) % 2 == 1:
            return True
        else:
            return False


    def print_board(self):
        padding = len(str(len(self.board) - 1))
        for i in range(self.size ** 2):
            print(str(self.board[i]).zfill(padding), end=" ")
            if (i + 1) % self.size == 0:
                print()

    def valid_moves(self):

        index_of_blank = self.board.index(0)

        left = (index_of_blank - 1, index_of_blank)
        right = (index_of_blank + 1, index_of_blank)
        up = (index_of_blank - self.size, index_of_blank)
        down = (index_of_blank + self.size, index_of_blank)

        moves = []

        if up[0] >= 0:
            moves.append(up)
        if right[0] % self.size != 0:
            moves.append(right)
        if down[0] <= self.size ** 2 - 1:
            moves.append(down)
        if left[0] % self.size != self.size - 1:
            moves.append(left)

        return moves

    def make_move(self, move):
        if move in self.valid_moves():
            self.board[move[0]], self.board[move[1]] = self.board[move[1]], self.board[move[0]]
            self.hash_board()
        else:
            print("wrong move")

    def is_win(self):
        for i in range(len(self.board)-1):
            if self.board[i] != i + 1:
                return False

        # if on index 0 is 1, on index 1 is 2 ... we solved a puzzle
        return True

    def manhattan_distance(self):

        whole_distance = 0
        for i in range(len(self.board)):
            element = self.board[i]

            row_of_element = i // self.size
            column_of_element = i % self.size

            proper_index = element - 1
            if element == 0:
                proper_index = len(self.board)-1

            proper_row = proper_index // self.size
            proper_col = proper_index % self.size

            diff_col = abs(column_of_element - proper_col)
            diff_row = abs(row_of_element - proper_row)

            dist = diff_col + diff_row

            whole_distance += dist

        return whole_distance

