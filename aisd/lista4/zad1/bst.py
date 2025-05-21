

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
        height = self.tree_height()
        self.left_trace = [' '] * (height + 1)
        self.right_trace = [' '] * (height + 1)
        print()
        self._print_BST(self.root, 0, '-')
        print()

    def _print_BST(self, node, depth, prefix):
        if node is None:
            return

        if node.left:
            self._print_BST(node.left, depth + 1, '/')

        if prefix == '/':
            self.left_trace[depth - 1] = '|'
        if prefix == '\\':
            self.right_trace[depth - 1] = ' '

        if depth == 0:
            print("-", end="")
        else:
            print(" ", end="")

        for i in range(depth - 1):
            if self.left_trace[i] == '|' or self.right_trace[i] == '|':
                print("| ", end="")
            else:
                print("  ", end="")

        if depth > 0:
            print(f"{prefix}-", end="")

        print(f"[{node.key}]")

        self.left_trace[depth] = ' '
        if node.right:
            self.right_trace[depth] = '|'
            self._print_BST(node.right, depth + 1, '\\')


if __name__ == "__main__":
    bst = BinarySearchTree()

    values_to_insert = [2, 4, 8, 7, 1]

    for num in values_to_insert:
        node = Node(num)
        print(f"INSERT: [{num}]\n")
        bst.insert_node(node)
        print("TREE:")
        bst.print_BST()
        print()