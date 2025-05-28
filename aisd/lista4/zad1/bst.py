import random
import sys
import time

big_tree = False

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class BinarySearchTree:
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

    def search(self, node, key):
        current = node
        while current is not None:
            self.current_comparisons += 1
            if key == current.key:
                return current
            self.current_comparisons += 1
            if key < current.key:
                current = current.left
                self.current_pointer_ops += 1
            else:
                current = current.right
                self.current_pointer_ops += 1
        return None

    def insert_node(self, z):
        self.reset_counters()
        y = None
        x = self.root
        self.current_pointer_ops += 1

        while x is not None:
            y = x
            self.current_comparisons += 1
            if z.key < x.key:
                x = x.left
                self.current_pointer_ops += 1
            else:
                x = x.right
                self.current_pointer_ops += 1

        z.parent = y
        self.current_pointer_ops += 1
        if y is None:
            self.root = z          # tree was empty
            self.current_pointer_ops += 1
        elif z.key < y.key:
            y.left = z
            self.current_pointer_ops += 1
            self.current_comparisons += 1
        else:
            y.right = z
            self.current_pointer_ops += 1
            self.current_comparisons += 1

        self.log_operation("insert")

        # replaces one subtree as a child of its parent with another subtree, needed for delete
    def transplant(self, u, v):
        self.current_pointer_ops += 1
        if u.parent is None:
            self.root = v
            self.current_pointer_ops += 1  # assign root
        elif u == u.parent.left:
            u.parent.left = v
            self.current_pointer_ops += 4  # condition plus previous line
        else:
            u.parent.right = v
            self.current_pointer_ops += 4  # we need to count condition also

        if v is not None:
            v.parent = u.parent
            self.current_pointer_ops += 2

    def tree_minimum(self, x):
        while x.left is not None:
            x = x.left
            self.current_pointer_ops += 2
        return x

    def tree_maximum(self, x):
        while x.right is not None:
            x = x.right
            self.current_pointer_ops += 2
        return x

    def delete_node(self, val_to_delete):
        self.reset_counters()

        z = self.search(self.root, val_to_delete)

        self.current_pointer_ops += 1
        if z.left is None:
            self.transplant(z, z.right)
            self.current_pointer_ops += 1
        elif z.right is None:
            self.transplant(z, z.left)
            self.current_pointer_ops += 2
        else:
            y = self.tree_minimum(z.right)
            self.current_pointer_ops += 2

            self.current_pointer_ops += 1
            if y.parent != z:
                self.transplant(y, y.right)
                y.right = z.right
                self.current_pointer_ops += 4
                if y.right is not None:
                    y.right.parent = y
                    self.current_pointer_ops += 2

            self.transplant(z, y)
            y.left = z.left
            self.current_pointer_ops += 3
            if y.left is not None:
                y.left.parent = y
                self.current_pointer_ops += 2

        self.log_operation("delete")

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

    def print_BST(self):
        if self.root is not None:
            print_tree(self.root, val='key')
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
        node_to_insert = Node(i)
        tree.insert_node(node_to_insert)
        if not big_tree:
            print()
            print("INSERT: ", i)
            tree.print_BST()
            print("Height: ", tree.tree_height())

def random_insert(tree, n):
    keys = list(range(1, n + 1))    # creating random permutation
    random.shuffle(keys)
    for key in keys:
        node_to_insert = Node(key)
        tree.insert_node(node_to_insert)
        if not big_tree:
            print()
            print("INSERT: ", key)
            tree.print_BST()
            print("Height: ", tree.tree_height())

def random_delete(tree, n):
    keys = list(range(1, n + 1))
    random.shuffle(keys)

    for key in keys:
        tree.delete_node(key)
        if not big_tree:
            print()
            print("DELETE: ", key)
            tree.print_BST()
            print("Height: ", tree.tree_height())

def metrics_cost(log):
    if not log:
        return 0, 0
    return sum(log)/len(log)

if __name__ == "__main__":

    if(len(sys.argv) != 2):
        print("Wrong number of arguments")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: n has to be an integer")
        sys.exit(1)

    if n > 30:
        big_tree = True

    bst = BinarySearchTree()

    start = time.time()

    print("----1 case: ascending_insert and random_delete for n =", n, "----")
    ascending_insert(bst, n)
    print("Ascending insert average cost comparisons: ", metrics_cost(bst.insert_comparisons_log))
    print("Ascending insert average cost pointer: ", metrics_cost(bst.insert_pointer_ops_log))
    print("Ascending insert average height: ", metrics_cost(bst.insert_heights_log))

    print("Ascending insert max comparisons: ", max(bst.insert_comparisons_log))
    print("Ascending insert max pointer: ", max(bst.insert_pointer_ops_log))
    print("Ascending insert max height: ", max(bst.insert_heights_log))

    random_delete(bst, n)
    print("Random delete average cost comparisons: ", metrics_cost(bst.delete_comparisons_log))
    print("Random delete average cost pointer: ", metrics_cost(bst.delete_pointer_ops_log))
    print("Random delete average height: ", metrics_cost(bst.delete_heights_log))

    print("Random delete max comparisons: ", max(bst.delete_comparisons_log))
    print("Random delete max pointer: ", max(bst.delete_pointer_ops_log))
    print("Random delete max height: ", max(bst.delete_heights_log))
    print()

    bst2 = BinarySearchTree()

    print("----2 case: random_insert and random_delete for n =", n, "----")
    random_insert(bst2, n)
    print("Random insert average cost comparisons: ", metrics_cost(bst2.insert_comparisons_log))
    print("Random insert average cost pointer: ", metrics_cost(bst2.insert_pointer_ops_log))
    print("Random insert average height: ", metrics_cost(bst2.insert_heights_log))

    print("Random insert max comparisons: ", max(bst2.insert_comparisons_log))
    print("Random insert max pointer: ", max(bst2.insert_pointer_ops_log))
    print("Random insert max height: ", max(bst2.insert_heights_log))

    random_delete(bst2, n)
    print("Random delete average cost comparisons: ", metrics_cost(bst2.delete_comparisons_log))
    print("Random delete average cost pointer: ", metrics_cost(bst2.delete_pointer_ops_log))
    print("Random delete average height: ", metrics_cost(bst2.delete_heights_log))

    print("Random delete max comparisons: ", max(bst2.delete_comparisons_log))
    print("Random delete max pointer: ", max(bst2.delete_pointer_ops_log))
    print("Random delete max height: ", max(bst2.delete_heights_log))
    end = time.time()

    print("Time elapsed: ", end - start)

