from Board import Board
import heapq

class AStar:
    def __init__(self, start):
        self.start = start

    def a_star_search(self):

        # check if we reached a destination
        if self.start.is_win():
            print("Puzzle solved")
            return


        # list with visited nodes
        closed_list = []

        self.start.f = 0
        self.start.g = 0
        self.start.h = 0

        # cells to be visited
        open_list = []
        heapq.heappush(open_list, (0, self.start))    # cost of going to start is 0

        found_dest = False

        while len(open_list) > 0:

            # Pop the node with the smallest f value from the open list
            p = heapq.heappop(open_list)

            current_node = p[1]

            # mark node as visited
            closed_list.append(current_node)

            moves = current_node.valid_moves()      # valid moves for this board layout

            for possible_move in moves:

                new_current_node = current_node.copy()
                new_current_node.move_that_was_made = possible_move
                new_current_node.make_move(possible_move)

                if not closed_list[possible_move]:
                    if current_node.is_win():

                        new_current_node.parent = current_node   # old move becomes a parent of a new node
                        print("Puzzle solved")
                        print(self.path(new_current_node))
                        found_dest = True
                        return
                    else:
                        g_new = current_node.g + 1
                        h_new = new_current_node.manhattan_distance()
                        f_new = g_new + h_new

                        if new_current_node.f == 0 or new_current_node.f > f_new:
                            heapq.heappush(open_list, (f_new, new_current_node))

                            new_current_node.g = g_new
                            new_current_node.h = h_new
                            new_current_node.f = f_new
                            new_current_node.parent = current_node


        if not found_dest:
            print("Failed to find a solution")

    def path(self, node):
        all_moves = []
        current = node

        while current.parent is not None:
            all_moves.append(current.move_that_was_made)
            current = current.parent

        all_moves.reverse()

        return all_moves

    # TO DO custom copy function


