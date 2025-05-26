import random
import sys

big_tree = False


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

        # counters for current operation
        self.current_comparisons = 0
        self.current_pointer_ops = 0

        # stats collection
        self.insert_comparisons_log = []
        self.insert_pointer_ops_log = []
        self.insert_heights_log = []

        self.delete_comparisons_log = []
        self.delete_pointer_ops_log = []
        self.delete_heights_log = []

    def reset_counters(self):
        self.current_comparisons = 0
        self.current_pointer_ops = 0

    def log_operation(self, op):
        if op == "delete":
            self.delete_comparisons_log.append(self.current_comparisons)
            self.delete_pointer_ops_log.append(self.current_pointer_ops)
            self.delete_heights_log.append(self.tree_height())
        elif op == "insert":
            self.insert_comparisons_log.append(self.current_comparisons)
            self.insert_pointer_ops_log.append(self.current_pointer_ops)
            self.insert_heights_log.append(self.tree_height())

    def tree_height(self):
        if not self.root:
            return 0
        max_height = 0
        stack = [(self.root, 1)]
        while stack:
            node, depth = stack.pop()
            if node:
                max_height = max(max_height, depth)
                stack.append((node.left, depth + 1))
                stack.append((node.right, depth + 1))
        return max_height

    def _rotate_right(self, pivot):
        new_root = pivot.left
        pivot.left = new_root.right
        new_root.right = pivot
        self.current_pointer_ops += 4
        return new_root

    def _rotate_left(self, pivot):
        new_root = pivot.right
        pivot.right = new_root.left
        new_root.left = pivot
        self.current_pointer_ops += 4
        return new_root

    def _splay(self, node, value):
        if node is None:
            return None

        self.current_comparisons += 1
        if node.value == value:
            return node

        self.current_comparisons += 1
        if value < node.value:
            self.current_pointer_ops += 1
            if node.left is None:
                return node
            self.current_comparisons += 1

            self.current_pointer_ops += 1
            if value < node.left.value:
                node.left.left = self._splay(node.left.left, value)
                node = self._rotate_right(node)
                self.current_pointer_ops += 4

            elif value > node.left.value:
                self.current_pointer_ops += 1
                self.current_comparisons += 1
                node.left.right = self._splay(node.left.right, value)
                self.current_pointer_ops += 6
                if node.left.right:
                    node.left = self._rotate_left(node.left)
                    self.current_pointer_ops += 2
            else:
                self.current_pointer_ops += 1
                self.current_comparisons += 1

            self.current_pointer_ops += 1
            if node.left is None:
                return node
            else:
                return self._rotate_right(node)
        else:
            self.current_pointer_ops += 1
            if node.right is None:
                return node

            self.current_comparisons += 1
            self.current_pointer_ops += 1
            if value > node.right.value:
                node.right.right = self._splay(node.right.right, value)
                node = self._rotate_left(node)
                self.current_pointer_ops += 4
            elif value < node.right.value:
                self.current_comparisons += 1
                self.current_pointer_ops += 1

                node.right.left = self._splay(node.right.left, value)
                self.current_pointer_ops += 6
                if node.right.left:
                    node.right = self._rotate_right(node.right)
                    self.current_pointer_ops += 2
            else:
                self.current_comparisons += 1
                self.current_pointer_ops += 1

            self.current_pointer_ops += 1
            if node.right is None:
                return node
            else:
                return self._rotate_left(node)

    def insert(self, value):
        self.reset_counters()

        self.current_pointer_ops += 1
        if self.root is None:
            self.root = Node(value)
            self.current_pointer_ops += 1
            return

        self.root = self._splay(self.root, value)
        self.current_pointer_ops += 2

        self.current_comparisons += 1
        self.current_pointer_ops += 1
        if self.root.value == value:
            return          # Already in tree

        new_node = Node(value)
        self.current_comparisons += 1
        self.current_pointer_ops += 1
        if value < self.root.value:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
            self.current_pointer_ops += 7
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
            self.current_pointer_ops += 7

        self.root = new_node
        self.current_pointer_ops += 1
        self.log_operation("insert")


    def search(self, value):
        self.root = self._splay(self.root, value)
        self.current_pointer_ops += 2

        self.current_pointer_ops += 1
        if self.root is not None:
            self.current_comparisons += 1
            self.current_pointer_ops += 1
            return self.root.value == value
        else:
            return False

    def delete(self, value):
        self.reset_counters()
        self.current_pointer_ops += 1
        if self.root is None:
            return

        self.root = self._splay(self.root, value)
        self.current_pointer_ops += 2

        self.current_comparisons += 1
        self.current_pointer_ops += 1
        if self.root.value != value:
            return  # Not found

        self.current_pointer_ops += 2
        if self.root.left is None:
            self.root = self.root.right
            self.current_pointer_ops += 3
        else:
            temp = self._splay(self.root.left, value)
            temp.right = self.root.right
            self.root = temp
            self.current_pointer_ops += 6

        self.log_operation("delete")

    def print_splay_tree(self):
        if self.root is not None:
            print_tree(self.root, val='value')
        else:
            print("(empty tree)")

def print_tree(root, val="val", left="left", right="right"):
    def display(root, val=val, left=left, right=right):
        # no children
        if getattr(root, right) is None and getattr(root, left) is None:
            line = '%s' % getattr(root, val)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # only left child
        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))       # recurrent in left child
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # only right child
        if getattr(root, left) is None:
            lines, n, p, x = display(getattr(root, right))      # recurrent in right child
            s = '%s' % getattr(root, val)                       # value of current node
            u = len(s)                                          # length of value
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        left_lines, n, p, x = display(getattr(root, left))
        right_lines, m, q, y = display(getattr(root, right))
        s = '%s' % getattr(root, val)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        # fill left and right tree
        if p < q:
            left_lines += [n * ' '] * (q - p)
        elif q < p:
            right_lines += [m * ' '] * (p - q)

        # merge two trees: left and right
        zipped_lines = zip(left_lines, right_lines)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    # calling display and writing a tree
    lines, *_ = display(root, val, left, right)
    for line in lines:
        print(line)


def ascending_insert(tree, n):
    for i in range(1, n + 1):
        tree.insert(i)
        if not big_tree:
            print()
            print("INSERT: ", i)
            tree.print_splay_tree()
            print("Height: ", tree.tree_height())

def random_insert(tree, n):
    keys = list(range(1, n + 1))    # creating random permutation
    random.shuffle(keys)
    for key in keys:
        tree.insert(key)
        if not big_tree:
            print()
            print("INSERT: ", key)
            tree.print_splay_tree()
            print("Height: ", tree.tree_height())

def random_delete(tree, n):
    keys = list(range(1, n + 1))
    random.shuffle(keys)

    for key in keys:
        tree.delete(key)
        if not big_tree:
            print()
            print("DELETE: ", key)
            tree.print_splay_tree()
            print("Height: ", tree.tree_height())

def metrics_cost(log):
    if not log:
        return 0, 0
    return sum(log)/len(log)

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Wrong number of arguments")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: n has to be an integer")
        sys.exit(1)

    if n > 30:
        big_tree = True

    tree1 = SplayTree()

    print("----1 case: ascending_insert and random_delete for n =", n, "----")
    ascending_insert(tree1, n)
    print("Ascending insert average cost comparisons: ", metrics_cost(tree1.insert_comparisons_log))
    print("Ascending insert average cost pointer: ", metrics_cost(tree1.insert_pointer_ops_log))
    print("Ascending insert average height: ", metrics_cost(tree1.insert_heights_log))

    print("Ascending insert max comparisons: ", max(tree1.insert_comparisons_log))
    print("Ascending insert max pointer: ", max(tree1.insert_pointer_ops_log))
    print("Ascending insert max height: ", max(tree1.insert_heights_log))

    random_delete(tree1, n)
    print("Random delete average cost comparisons: ", metrics_cost(tree1.delete_comparisons_log))
    print("Random delete average cost pointer: ", metrics_cost(tree1.delete_pointer_ops_log))
    print("Random delete average height: ", metrics_cost(tree1.delete_heights_log))


    print("Random delete max comparisons: ", max(tree1.delete_comparisons_log))
    print("Random delete max pointer: ", max(tree1.delete_pointer_ops_log))
    print("Random delete max height: ", max(tree1.delete_heights_log))
    print()

    tree2 = SplayTree()

    print("----2 case: random_insert and random_delete for n =", n, "----")
    random_insert(tree2, n)
    print("Random insert average cost comparisons: ", metrics_cost(tree2.insert_comparisons_log))
    print("Random insert average cost pointer: ", metrics_cost(tree2.insert_pointer_ops_log))
    print("Random insert average height: ", metrics_cost(tree2.insert_heights_log))

    print("Random insert max comparisons: ", max(tree2.insert_comparisons_log))
    print("Random insert max pointer: ", max(tree2.insert_pointer_ops_log))
    print("Random insert max height: ", max(tree2.insert_heights_log))

    random_delete(tree2, n)
    print("Random delete average cost comparisons: ", metrics_cost(tree2.delete_comparisons_log))
    print("Random delete average cost pointer: ", metrics_cost(tree2.delete_pointer_ops_log))
    print("Random delete average height: ", metrics_cost(tree2.delete_heights_log))

    print("Random delete max comparisons: ", max(tree2.delete_comparisons_log))
    print("Random delete max pointer: ", max(tree2.delete_pointer_ops_log))
    print("Random delete max height: ", max(tree2.delete_heights_log))