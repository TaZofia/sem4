import random
import sys

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.left_trace = []
        self.right_trace = []

    def search(self, node, key):
        if node is None or key == node.key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

    def insert_node(self, z):
        y = None
        x = self.root

        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y is None:
            self.root = z          # tree was empty
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

    # replaces one subtree as a child of its parent with another subtree, needed for delete
    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def tree_minimum(self, x):
        while x.left is not None:
            x = x.left
        return x

    def tree_maximum(self, x):
        while x.right is not None:
            x = x.right
        return x

    def delete_node(self, z):
        if z.left is None:
            self.transplant(z, z.right)
        elif z.right is None:
            self.transplant(z, z.left)
        else:
            y = self.tree_minimum(z.right)
            if y.parent != z:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y

    def tree_height(self, x=None):
        if x is None:
            x = self.root       # if we didn't precise where we start, we start counting height from root
        if x is None:
            return 0
        return 1 + max(self.tree_height(x.left), self.tree_height(x.right))

    def print_BST(self):
        if self.root is not None:
            print_tree(self.root, val='key')
        else:
            print("(empty tree)")

def print_tree(root, val="val", left="left", right="right"):
    def display(root, val=val, left=left, right=right):
        if getattr(root, right) is None and getattr(root, left) is None:
            line = '%s' % getattr(root, val)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        if getattr(root, left) is None:
            lines, n, p, x = display(getattr(root, right))
            s = '%s' % getattr(root, val)
            u = len(s)
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
        if p < q:
            left_lines += [n * ' '] * (q - p)
        elif q < p:
            right_lines += [m * ' '] * (p - q)
        zipped_lines = zip(left_lines, right_lines)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    lines, *_ = display(root, val, left, right)
    for line in lines:
        print(line)

def ascending_insert(tree, n):
    for i in range(1, n + 1):
        node_to_insert = Node(i)
        tree.insert_node(node_to_insert)
        print()
        print("Insert: ", i)
        tree.print_BST()
        print("Height: ", tree.tree_height(tree.root))

def random_insert(tree, n):
    keys = list(range(1, n + 1))    # creating random permutation
    random.shuffle(keys)
    for key in keys:
        node_to_insert = Node(key)
        tree.insert_node(node_to_insert)
        print()
        print("Insert: ", key)
        tree.print_BST()
        print("Height: ", tree.tree_height(tree.root))

def random_delete(tree, n):
    keys = list(range(1, n + 1))
    random.shuffle(keys)

    for key in keys:
        node_to_delete = tree.search(tree.root, key)
        if node_to_delete is not None:
            tree.delete_node(node_to_delete)
            print()
            print("Delete: ", key)
            tree.print_BST()
            print("Height: ", tree.tree_height(tree.root))



if __name__ == "__main__":

    if(len(sys.argv) != 2):
        print("Wrong number of arguments")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: n has to be an integer")
        sys.exit(1)


    bst1 = BinarySearchTree()

    
    print("---1 case: ascending_insert and random_delete for n =", n, "----")
    ascending_insert(bst1, n)
    random_delete(bst1, n)

    print("---2 case: random_insert and random_delete for n =", n, "----")
    random_insert(bst1, n)
    random_delete(bst1, n)
