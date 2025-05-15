from AStar import AStar
from Board import Board
import time
import random

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

    '''
    size = 3

    while True:
        my_board = Board(size)
        if my_board.can_be_solved():
            break

    my_board.print_board()

    astar = AStar(my_board)
    time_start = time.time()
    result = astar.a_star_search()
    time_end = time.time()

    if result == None:
        print("No solution found.")
    else:
        print("Puzzle solved!")
        print(result)
        print("Number of moves: " , len(result))
        print("Time elapsed: " + str(time_end - time_start))
    '''
    size = 4

    my_board = Board(size)

    my_board.board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    my_board.hash_board()

    previous_move = None
    inverse_move = None

    for i in range(30):
        moves = my_board.valid_moves()
        while True:
            index = random.randint(0, len(moves) - 1)
            move = moves[index]
            if move != inverse_move:
                break

        my_board.make_move(move)
        previous_move = move
        inverse_move = (previous_move[1], previous_move[0])


    my_board.print_board()

    astar = AStar(my_board)
    time_start = time.time()
    result = astar.a_star_search()
    time_end = time.time()

    if result == None:
        print("No solution found.")
    else:
        print("Puzzle solved!")
        print(result)
        print("Number of moves: " , len(result))
        print("Time elapsed: " + str(time_end - time_start))


if __name__ == "__main__":
    main()
