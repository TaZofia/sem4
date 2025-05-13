from sklearn.utils.arrayfuncs import cholesky_delete

from AStar import AStar
from Board import Board
from Manhattan import Manhattan

def get_user_input():
    while True:
        try:
            size = int(input("Enter board size: "))
            if size >= 2:
                return size
            else:
                print("Board size must be at least 2.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def main():

    size = 3

    while True:
        my_board = Board(size)
        if my_board.can_be_solved():
            break

    my_board.print_board()

    astar = AStar(my_board)
    astar.a_star_search()



if __name__ == "__main__":
    main()
