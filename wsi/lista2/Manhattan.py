from Board import Board

class Manhattan:
    def __init__(self, board_obj):
        self.board_obj = board_obj

    def distance(self, element):          # element in the array - value
        index_of_element = self.board_obj.board.index(element)

        row_of_element = index_of_element // self.board_obj.size
        column_of_element = index_of_element % self.board_obj.size

        proper_index = element - 1      # because first index in array equals 0
        if element == 0:
            proper_index = 15

        proper_row = proper_index // self.board_obj.size
        proper_col = proper_index % self.board_obj.size

        diff_col = abs(column_of_element - proper_col)
        diff_row = abs(row_of_element - proper_row)

        return diff_col + diff_row

