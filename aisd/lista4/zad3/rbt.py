
RED = "\033[31m"
RESET = "\033[0m"


def visible_len(s):
    return len(s.replace(RED, '').replace(RESET, ''))

class Node:
    # Constructor to initialize node of RB Tree
    def __init__(self, value, color='red'):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    # function to get the grandparent of node
    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # function to get the sibling of node
    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    # function to get the uncle of node
    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()

# Class to implement Red Black Tree
class RedBlackTree:
    def __init__(self):
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

        self.NIL = Node(None)
        self.NIL.color = 'black'
        self.NIL.left = self.NIL.right = self.NIL.parent = self.NIL

        self.root = self.NIL

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

    def search(self, node, val_to_search):
        while node != self.NIL:
            self.current_comparisons += 1
            if val_to_search == node.value:
                return node
            self.current_comparisons += 1
            if val_to_search < node.value:
                node = node.left
                self.current_pointer_ops += 1
            else:
                node = node.right
                self.current_pointer_ops += 1
        return self.NIL

    def tree_height(self):
        print("in")
        if not self.root:
            return 0
        max_height = 0
        stack = [(self.root, 1)]
        while stack:
            node, depth = stack.pop()
            if node != self.NIL:
                max_height = max(max_height, depth)
                stack.append((node.left, depth + 1))
                stack.append((node.right, depth + 1))
        return max_height

    def tree_minimum(self, x):
        while x.left != self.NIL:
            self.current_pointer_ops += 1       # while
            x = x.left
            self.current_pointer_ops += 1       # line before
        return x

    # Function to fix the Red Black Tree properties after insertion
    def insert_fix(self, z):
        while z.parent.color == 'red':
            self.current_pointer_ops += 1
            self.current_pointer_ops += 3
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                self.current_pointer_ops += 3

                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                    self.current_pointer_ops += 5
                else:
                    self.current_pointer_ops += 2
                    if z == z.parent.right:
                        z = z.parent
                        self.current_pointer_ops += 1
                        self.rotate_left(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.rotate_right(z.parent.parent)
                    self.current_pointer_ops += 5
            else:
                y = z.parent.parent.left
                self.current_pointer_ops += 3
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                    self.current_pointer_ops += 5
                else:
                    self.current_pointer_ops += 2
                    if z == z.parent.left:
                        z = z.parent
                        self.current_pointer_ops += 1
                        self.rotate_right(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.rotate_left(z.parent.parent)
                    self.current_pointer_ops += 5
        self.root.color = 'black'
        self.current_pointer_ops += 1


    # function to insert a node similar to BST insertion
    def insert(self, val_to_insert):
        # add new node
        z = Node(val_to_insert)

        y = self.NIL
        x = self.root
        self.current_pointer_ops += 1
        while x != self.NIL:
            y = x
            self.current_comparisons += 1
            if z.value < x.value:
                x = x.left
                self.current_pointer_ops += 1
            else:
                x = x.right
                self.current_pointer_ops += 1
        z.parent = y
        self.current_pointer_ops += 1
        if y == self.NIL:
            self.root = z
            self.current_pointer_ops += 1
            z.color = 'black'
        elif z.value < y.value:
            y.left = z
            self.current_pointer_ops += 1
            self.current_comparisons += 1
        else:
            y.right = z
            self.current_pointer_ops += 1
            self.current_comparisons += 1

        z.left = self.NIL
        z.right = self.NIL
        self.current_pointer_ops += 2
        z.color = 'red'
        self.insert_fix(z)

    # function for left rotation of RB Tree
    def rotate_left(self, x):
        y = x.right         # set y
        x.right = y.left    # turn y's left subtree into x's right subtree
        self.current_pointer_ops += 4
        if y.left != self.NIL:
            y.left.parent = x
            self.current_pointer_ops += 2
        y.parent = x.parent
        self.current_pointer_ops += 3
        if x.parent == self.NIL:
            self.root = y
            self.current_pointer_ops += 1
        elif x == x.parent.left:
            x.parent.left = y
            self.current_pointer_ops += 4       # condition plus operation inside elif
        else:
            x.parent.right = y
            self.current_pointer_ops += 4

        y.left = x      # put x on y's left
        x.parent = y
        self.current_pointer_ops += 2


    # function for right rotation of RB Tree
    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        self.current_pointer_ops += 4
        if y.right != self.NIL:
            y.right.parent = x
            self.current_pointer_ops += 2
        y.parent = x.parent
        self.current_pointer_ops += 3
        if x.parent == self.NIL:
            self.root = y
            self.current_pointer_ops += 1
        elif x == x.parent.right:
            x.parent.right = y
            self.current_pointer_ops += 4
        else:
            x.parent.left = y
            self.current_pointer_ops += 4

        y.right = x
        x.parent = y
        self.current_pointer_ops += 2


    def rb_transplant(self, u, v):
        self.current_pointer_ops += 1
        if u.parent == self.NIL:
            self.root = v
            self.current_pointer_ops += 1
        elif u == u.parent.left:
            u.parent.left = v
            self.current_pointer_ops += 4
        else:
            u.parent.right = v
            self.current_pointer_ops += 4

        v.parent = u.parent
        self.current_pointer_ops += 2

    def delete(self, value):
        z = self.search(self.root, value)

        y = z
        y_original_color = y.color
        self.current_pointer_ops += 1
        if z.left == self.NIL:
            x = z.right
            self.rb_transplant(z, z.right)
            self.current_pointer_ops += 2
        elif z.right == self.NIL:
            x = z.left
            self.rb_transplant(z, z.left)
            self.current_pointer_ops += 3
        else:
            y = self.tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            self.current_pointer_ops += 4
            if y.parent == z:
                x.parent = y
                self.current_pointer_ops += 1
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                self.current_pointer_ops += 5

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            self.current_pointer_ops += 4

        if y_original_color == 'black':
            self.delete_fix(x)

    def delete_fix(self, x):
        while x != self.root and x.color == 'black':
            self.current_pointer_ops += 3
            if x == x.parent.left:
                w = x.parent.right
                self.current_pointer_ops += 2
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_left(x.parent)
                    w = x.parent.right
                    self.current_pointer_ops += 4

                self.current_pointer_ops += 2
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                    self.current_pointer_ops += 1
                else:
                    self.current_pointer_ops += 1
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.rotate_right(w)
                        w = x.parent.right
                        self.current_pointer_ops += 3

                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self.rotate_left(x.parent)
                    x = self.root
                    self.current_pointer_ops += 5
            else:
                w = x.parent.left
                self.current_pointer_ops += 2
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_right(x.parent)
                    w = x.parent.left
                    self.current_pointer_ops += 4

                self.current_pointer_ops += 2
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                    self.current_pointer_ops += 1
                else:
                    self.current_pointer_ops += 1
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.rotate_left(w)
                        w = x.parent.left
                        self.current_pointer_ops += 3

                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self.rotate_right(x.parent)
                    x = self.root
                    self.current_pointer_ops += 5
        x.color = 'black'

    def print_rbt_tree(self):
        if self.root != self.NIL:
            print_tree(self.root, val='value', NIL=self.NIL)
        else:
            print("(empty tree)")


def print_tree(root, val="value", left="left", right="right", NIL=None):
    def display(root, val=val, left=left, right=right):
        # no children - leafs
        if getattr(root, right) == NIL and getattr(root, left) == NIL:
            color = getattr(root, 'color', 'black')
            s = f"{RED}{getattr(root, val)}{RESET}" if color == 'red' else f"{getattr(root, val)}"
            width = visible_len(s)
            height = 1
            middle = width // 2
            return [s], width, height, middle

        # only left child
        if getattr(root, right) == NIL:
            lines, n, p, x = display(getattr(root, left))       # recurrent in left child
            color = getattr(root, 'color', 'black')
            s = f"{RED}{getattr(root, val)}{RESET}" if color == 'red' else f"{getattr(root, val)}"
            u = visible_len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # only right child
        if getattr(root, left) == NIL:
            lines, n, p, x = display(getattr(root, right))      # recurrent in right child
            color = getattr(root, 'color', 'black')
            s = f"{RED}{getattr(root, val)}{RESET}" if color == 'red' else f"{getattr(root, val)}"
            u = visible_len(s)                                          # length of value
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        left_lines, n, p, x = display(getattr(root, left))
        right_lines, m, q, y = display(getattr(root, right))
        color = getattr(root, 'color', 'black')
        s = f"{RED}{getattr(root, val)}{RESET}" if color == 'red' else f"{getattr(root, val)}"
        u = visible_len(s)
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



if __name__ == "__main__":
    tree = RedBlackTree()

    for i in range(100000):
        tree.insert(i)

    print("tree height: ", tree.tree_height())

    print("done")

