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

    '''
    while True:
        my_board = Board(size)
        if my_board.can_be_solved():
            break


    my_board.print_board()
    child = Board(size, my_board)

    child.board = my_board.board.copy()
    child.make_move(my_board.valid_moves()[0])

    child.print_board()
    print("////")
    my_board.print_board()
    
    my_board = Board(size)
    my_board.board = [1, 2, 3, 4, 6, 5, 7, 8, 0]

    astar = AStar(my_board)

    astar.a_star_search()
    '''
    my_board = Board(size)
    my_board.board = [1, 2, 0, 4, 6, 5, 7, 8, 3]
    my_board.print_board()

    print(my_board.manhattan_distance())


if __name__ == "__main__":
    main()
