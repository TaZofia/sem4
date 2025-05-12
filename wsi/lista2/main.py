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
    # size = get_user_input()
    size = 3

    my_board = Board(size)
    my_board.board = [1, 2, 3, 4, 5, 6, 7, 0, 8]

    astar = AStar(my_board)
    astar.a_star_search()


if __name__ == "__main__":
    main()
