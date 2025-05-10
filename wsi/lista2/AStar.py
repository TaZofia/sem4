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

        # TO DO details

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
                if not closed_list[possible_move]:
                    if current_node.is_win():
                        # TO DO details
                        print("Puzzle solved")
                        found_dest = True
                        return
                    else:

# TO DO detailks not in list - should be in board class, f, g, h
