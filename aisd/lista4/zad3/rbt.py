
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

    def search(self, node, val_to_search):
        current = node
        while current is not None:
            self.current_comparisons += 1
            if val_to_search == current.value:
                return current
            self.current_comparisons += 1
            if val_to_search < current.value:
                current = current.left
                self.current_pointer_ops += 1
            else:
                current = current.right
                self.current_pointer_ops += 1
        return None

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
    def tree_minimum(self, x):
        while x.left is not None:
            x = x.left
            self.current_pointer_ops += 1
        return x

    # Function to fix the Red Black Tree properties after insertion
    def insert_fix(self, z):
        while z.parent is not None and z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y is not None and y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.rotate_left(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y is not None and y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.rotate_right(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.rotate_left(z.parent.parent)

        self.root.color = 'black'


    # function to insert a node similar to BST insertion
    def insert(self, val_to_insert):
        z = Node(val_to_insert)
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
            z.color = 'black'
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z
        z.left = None
        z.right = None
        z.color = 'red'
        self.insert_fix(z)

    # function for left rotation of RB Tree
    def rotate_left(self, x):
        y = x.right         # set y
        x.right = y.left    # turn y's left subtree into x's right subtree
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x      # put x on y's left
        x.parent = y


    # function for right rotation of RB Tree
    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y


    def rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def delete(self, value):
        z = self.search(self.root, value)
        if z is None:       # no exist
            return
        y = z
        y_original_color = y.color
        if z.left is None:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right is None:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 'black':
            self.delete_fix(x)


    def delete_fix(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'  # Case 1
                    x.parent.color = 'red'  # Case 1
                    self.rotate_left(x.parent)  # Case 1
                    w = x.parent.right  # Update w

                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'  # Case 2
                    x = x.parent  # Move up the tree
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'  # Case 3
                        w.color = 'red'  # Case 3
                        self.rotate_right(w)  # Case 3
                        w = x.parent.right  # Update w

                    w.color = x.parent.color  # Case 4
                    x.parent.color = 'black'  # Case 4
                    w.right.color = 'black'  # Case 4
                    self.rotate_left(x.parent)  # Case 4
                    x = self.root  # Terminate loop
            else:
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'  # Case 1 (mirror)
                    x.parent.color = 'red'  # Case 1 (mirror)
                    self.rotate_right(x.parent)  # Case 1 (mirror)
                    w = x.parent.left  # Update w

                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'  # Case 2 (mirror)
                    x = x.parent  # Move up the tree
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'  # Case 3 (mirror)
                        w.color = 'red'  # Case 3 (mirror)
                        self.rotate_left(w)  # Case 3 (mirror)
                        w = x.parent.left  # Update w

                    w.color = x.parent.color  # Case 4 (mirror)
                    x.parent.color = 'black'  # Case 4 (mirror)
                    w.left.color = 'black'  # Case 4 (mirror)
                    self.rotate_right(x.parent)  # Case 4 (mirror)
                    x = self.root  # Terminate loop

        x.color = 'black'


    # function to replace an old node with a new node
    def _replace_node(self, old_node, new_node):
        if old_node.parent is None:
            self.root = new_node
        else:
            if old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
        if new_node is not None:
            new_node.parent = old_node.parent

    # function to find node with minimum value in a subtree
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    # function to perform inorder traversal
    def _inorder_traversal(self, node):
        if node is not None:
            self._inorder_traversal(node.left)
            print(node.value, end=" ")
            self._inorder_traversal(node.right)
    def print_rbt_tree(self):
        if self.root is not None:
            print_tree(self.root, val='value')
        else:
            print("(empty tree)")


def print_tree(root, val="value", left="left", right="right"):
    def display(root, val=val, left=left, right=right):
        # no children - leafs
        if getattr(root, right) is None and getattr(root, left) is None:
            color = getattr(root, 'color', 'black')
            s = f"{RED}{getattr(root, val)}{RESET}" if color == 'red' else f"{getattr(root, val)}"
            width = visible_len(s)
            height = 1
            middle = width // 2
            return [s], width, height, middle

        # only left child
        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))       # recurrent in left child
            color = getattr(root, 'color', 'black')
            s = f"{RED}{getattr(root, val)}{RESET}" if color == 'red' else f"{getattr(root, val)}"
            u = visible_len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # only right child
        if getattr(root, left) is None:
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

def print_colors(node):
    if node is None:
        return
    print(f"Node {node.value}, color: {node.color}")
    print_colors(node.left)
    print_colors(node.right)


if __name__ == "__main__":
    tree = RedBlackTree()

    values = [41, 38, 31, 12, 19, 8]
    for value in values:
        tree.insert(value)
        print(value)

    tree.print_rbt_tree()
    tree.delete(19)
    tree.print_rbt_tree()

