import random
class Board:

    def __init__(self, size):
        self.size = size        # size - number of elements in row/column
        self.board = []
        self._generate_perm()


    def _generate_perm(self):
        for i in range((self.size ** 2) - 1):
            self.board.append(i + 1)

        random.shuffle(self.board)
        self.board.append(0)


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
        if (self._number_of_inversions() + self._get_blank_row_number()) % 2 == 0:
            return True
        else:
            return False


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

        index_of_blank = self.board.index(0)

        left = index_of_blank - 1
        right = index_of_blank + 1
        up = index_of_blank - self.size
        down = index_of_blank + self.size

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
