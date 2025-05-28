#include <iostream>
#include <cstdlib>
#include <random>
#include <chrono>
#include <numeric>
#include <vector>
#include <sstream>
#include <algorithm>

using namespace std;

bool big_tree = false;

enum Operation {INSERT, DELETE};
enum Color {RED, BLACK};

string RED_ANSI = "\033[31m";
string RESET_ANSI = "\033[0m";

class Node {
public:
    int value;
    Color color;
    Node* left;
    Node* right;
    Node* parent;
    int height;

    // normal constructor
    Node(int val)
        : value(val), color(RED), left(getNIL()), right(getNIL()), parent(getNIL()), height(1) {}

    // constructor for NIL
    Node(int val, bool is_nil)
      : value(val), color(BLACK), left(nullptr), right(nullptr), parent(nullptr), height(0) {}

    static Node* getNIL() {
        static Node* NIL = []() {
            Node* nil = new Node(0, true);  // second constructor
            nil->left = nil;
            nil->right = nil;
            nil->parent = nil;
            return nil;
        }();
        return NIL;
    }
    // Returns grandparent of the node
    Node* grandparent() const {
        if (parent == getNIL()) return getNIL();
        return parent->parent;
    }

    // Returns sibling of the node
    Node* sibling() const {
        if (parent == getNIL()) return getNIL();
        if (this == parent->left) return parent->right;
        return parent->left;
    }

    // Returns uncle of the node
    Node* uncle() const {
        if (parent == getNIL()) return getNIL();
        return parent->sibling();
    }

};

class RedBlackTree {
public:
    Node* root;

    // counters for current operation
    int current_comparisons = 0;
    int current_pointer_ops = 0;

    // stats collection
    vector<int> insert_comparisons;
    vector<int> insert_pointer_ops;
    vector<int> insert_heights;

    vector<int> delete_comparisons;
    vector<int> delete_pointer_ops;
    vector<int> delete_heights;

    RedBlackTree() {
        root = Node::getNIL();
    }

    void reset_counters() {
        current_comparisons = 0;
        current_pointer_ops = 0;
    }

    int node_height(Node* node) {
        if (node == Node::getNIL()) return 0;
        return node->height;
    }

    void update_height(Node* node) {
        if (node != Node::getNIL()) {
            node->height = 1 + max(node_height(node->left), node_height(node->right));
        }
    }
    void update_height_upwards(Node* node) {
        while (node != Node::getNIL()) {
            update_height(node);
            node = node->parent;
        }
    }

    int tree_height() {
        return root->height;
    }

    void log_operation(Operation op) {
        if(op == INSERT) {
            insert_comparisons.push_back(current_comparisons);
            insert_pointer_ops.push_back(current_pointer_ops);
            insert_heights.push_back(tree_height());
        }
        else if(op == DELETE) {
            delete_comparisons.push_back(current_comparisons);
            delete_pointer_ops.push_back(current_pointer_ops);
            delete_heights.push_back(tree_height());
        }
    }
    Node* search(Node* node, int val_to_search) {
        while (node != Node::getNIL()) {
            current_comparisons++;
            if (val_to_search == node->value) {
                return node;
            }
            current_comparisons++;
            if (val_to_search < node->value) {
                node = node->left;
                current_pointer_ops++;
            } else {
                node = node->right;
                current_pointer_ops++;
            }
        }
        return Node::getNIL();
    }
    Node* tree_minimum(Node* x) {
        while (x->left != Node::getNIL()) {
            current_pointer_ops++; // while
            x = x->left;
            current_pointer_ops++; // line before
        }
        return x;
    }

    // Left rotation
    void rotate_left(Node* x) {
        Node* y = x->right; // set y
        x->right = y->left; // turn y's left subtree into x's right subtree
        current_pointer_ops += 4;

        if (y->left != Node::getNIL()) {
            y->left->parent = x;
            current_pointer_ops += 2;
        }

        y->parent = x->parent;
        current_pointer_ops += 3;

        if (x->parent == Node::getNIL()) {
            root = y;
            current_pointer_ops += 1;
        } else if (x == x->parent->left) {
            x->parent->left = y;
            current_pointer_ops += 4; // condition + assignment
        } else {
            x->parent->right = y;
            current_pointer_ops += 4;
        }

        y->left = x;     // put x on y's left
        x->parent = y;
        update_height(x);
        update_height(y);
        current_pointer_ops += 2;
    }

    // Right rotation
    void rotate_right(Node* x) {
        Node* y = x->left;
        x->left = y->right;
        current_pointer_ops += 4;

        if (y->right != Node::getNIL()) {
            y->right->parent = x;
            current_pointer_ops += 2;
        }

        y->parent = x->parent;
        current_pointer_ops += 3;

        if (x->parent == Node::getNIL()) {
            root = y;
            current_pointer_ops += 1;
        } else if (x == x->parent->right) {
            x->parent->right = y;
            current_pointer_ops += 4;
        } else {
            x->parent->left = y;
            current_pointer_ops += 4;
        }

        y->right = x;
        x->parent = y;
        update_height(x);
        update_height(y);
        current_pointer_ops += 2;
    }

    void insert_fix(Node* z) {
        while (z->parent->color == RED) {
            current_pointer_ops += 1;
            current_pointer_ops += 4;

            if (z->parent == z->parent->parent->left) {
                Node* y = z->parent->parent->right;
                current_pointer_ops += 3;

                if (y->color == RED) {
                    z->parent->color = BLACK;
                    y->color = BLACK;
                    z->parent->parent->color = RED;
                    z = z->parent->parent;
                    current_pointer_ops += 5;
                } else {
                    current_pointer_ops += 2;
                    if (z == z->parent->right) {
                        z = z->parent;
                        current_pointer_ops += 1;
                        rotate_left(z);
                    }
                    z->parent->color = BLACK;
                    z->parent->parent->color = RED;
                    rotate_right(z->parent->parent);
                    current_pointer_ops += 5;
                }
            } else {
                Node* y = z->parent->parent->left;
                current_pointer_ops += 3;

                if (y->color == RED) {
                    z->parent->color = BLACK;
                    y->color = BLACK;
                    z->parent->parent->color = RED;
                    z = z->parent->parent;
                    current_pointer_ops += 5;
                } else {
                    current_pointer_ops += 2;
                    if (z == z->parent->left) {
                        z = z->parent;
                        current_pointer_ops += 1;
                        rotate_right(z);
                    }
                    z->parent->color = BLACK;
                    z->parent->parent->color = RED;
                    rotate_left(z->parent->parent);
                    current_pointer_ops += 5;
                }
            }
        }
        root->color = BLACK;
        current_pointer_ops += 1;
    }

    void insert(int val_to_insert) {
        reset_counters();

        Node* z = new Node(val_to_insert);  // new node

        Node* y = Node::getNIL();
        Node* x = root;
        current_pointer_ops += 1;

        while (x != Node::getNIL()) {
            y = x;
            current_comparisons += 1;
            if (z->value < x->value) {
                x = x->left;
                current_pointer_ops += 1;
            } else {
                x = x->right;
                current_pointer_ops += 1;
            }
        }

        z->parent = y;
        current_pointer_ops += 1;

        if (y == Node::getNIL()) {
            root = z;
            current_pointer_ops += 1;
            z->color = BLACK;
        } else if (z->value < y->value) {
            y->left = z;
            current_pointer_ops += 1;
            current_comparisons += 1;
        } else {
            y->right = z;
            current_pointer_ops += 1;
            current_comparisons += 1;
        }

        z->left = Node::getNIL();
        z->right = Node::getNIL();
        current_pointer_ops += 2;
        z->color = RED;

        insert_fix(z);

        update_height_upwards(z);
        log_operation(INSERT);
    }

    void delete_fix(Node* x) {
        while (x != root && x->color == BLACK) {
            current_pointer_ops += 3;

            if (x == x->parent->left) {
                Node* w = x->parent->right;
                current_pointer_ops += 2;

                if (w->color == RED) {
                    w->color = BLACK;
                    x->parent->color = RED;
                    rotate_left(x->parent);
                    w = x->parent->right;
                    current_pointer_ops += 4;
                }

                current_pointer_ops += 2;
                if (w->left->color == BLACK && w->right->color == BLACK) {
                    w->color = RED;
                    x = x->parent;
                    current_pointer_ops += 1;
                } else {
                    current_pointer_ops += 1;
                    if (w->right->color == BLACK) {
                        w->left->color = BLACK;
                        w->color = RED;
                        rotate_right(w);
                        w = x->parent->right;
                        current_pointer_ops += 3;
                    }

                    w->color = x->parent->color;
                    x->parent->color = BLACK;
                    w->right->color = BLACK;
                    rotate_left(x->parent);
                    x = root;
                    current_pointer_ops += 5;
                }
            } else {
                Node* w = x->parent->left;
                current_pointer_ops += 2;

                if (w->color == RED) {
                    w->color = BLACK;
                    x->parent->color = RED;
                    rotate_right(x->parent);
                    w = x->parent->left;
                    current_pointer_ops += 4;
                }

                current_pointer_ops += 2;
                if (w->right->color == BLACK && w->left->color == BLACK) {
                    w->color = RED;
                    x = x->parent;
                    current_pointer_ops += 1;
                } else {
                    current_pointer_ops += 1;
                    if (w->left->color == BLACK) {
                        w->right->color = BLACK;
                        w->color = RED;
                        rotate_left(w);
                        w = x->parent->left;
                        current_pointer_ops += 3;
                    }

                    w->color = x->parent->color;
                    x->parent->color = BLACK;
                    w->left->color = BLACK;
                    rotate_right(x->parent);
                    x = root;
                    current_pointer_ops += 5;
                }
            }
        }

        x->color = BLACK;
    }

    void rb_transplant(Node* u, Node* v) {
        current_pointer_ops += 1;

        if (u->parent == Node::getNIL()) {
            root = v;
            current_pointer_ops += 1;
        } else if (u == u->parent->left) {
            u->parent->left = v;
            current_pointer_ops += 4;
        } else {
            u->parent->right = v;
            current_pointer_ops += 4;
        }

        v->parent = u->parent;
        current_pointer_ops += 2;
    }

    void delete_node(int value) {
        reset_counters();

        Node* z = search(root, value);

        Node* y = z;
        Color y_original_color = y->color;
        current_pointer_ops += 1;

        Node* x;

        if (z->left == Node::getNIL()) {
            x = z->right;
            rb_transplant(z, z->right);
            current_pointer_ops += 2;
        } else if (z->right == Node::getNIL()) {
            x = z->left;
            rb_transplant(z, z->left);
            current_pointer_ops += 3;
        } else {
            y = tree_minimum(z->right);
            y_original_color = y->color;
            x = y->right;
            current_pointer_ops += 4;

            if (y->parent == z) {
                x->parent = y;
                current_pointer_ops += 1;
            } else {
                rb_transplant(y, y->right);
                y->right = z->right;
                y->right->parent = y;
                current_pointer_ops += 5;
            }

            rb_transplant(z, y);
            y->left = z->left;
            y->left->parent = y;
            y->color = z->color;
            current_pointer_ops += 4;
        }

        if (y_original_color == BLACK) {
            delete_fix(x);
        }

        if (x != Node::getNIL()) {
            update_height_upwards(x->parent);
        } else if (y != Node::getNIL()) {
            update_height_upwards(y->parent);
        }

        log_operation(DELETE);
    }
};

int visible_len(const string& s) {
    string result;
    bool in_escape = false;
    for (size_t i = 0; i < s.size(); ++i) {
        if (s[i] == '\033') in_escape = true;
        if (!in_escape) result += s[i];
        if (in_escape && s[i] == 'm') in_escape = false;
    }
    return result.length();
}

string to_string_node(Node* node) {
    if (node == Node::getNIL()) return "NIL";
    stringstream ss;
    if (node->color == RED) {
        ss << RED_ANSI << node->value << RESET_ANSI;
    } else {
        ss << node->value;
    }
    return ss.str();
}
vector<string> display(Node* root, int& width, int& height, int& middle) {
  if (root == Node::getNIL()) {
      width = 0;
      height = 0;
      middle = 0;
      return {};
  }

  string s = to_string_node(root);
  int u = visible_len(s);

  // No children
  if (root->left == Node::getNIL() && root->right == Node::getNIL()) {
      width = u;
      height = 1;
      middle = u / 2;
      return { s };
  }

  // Only left child
  if (root->right == Node::getNIL()) {
      int n, p, x;
      vector<string> left_lines = display(root->left, n, p, x);
      string first_line = string(x + 1, ' ') + string(n - x - 1, '_') + s;
      string second_line = string(x, ' ') + '/' + string(n - x - 1 + u, ' ');

      vector<string> shifted_lines;
      for (const string& line : left_lines)
          shifted_lines.push_back(line + string(u, ' '));

      width = n + u;
      height = p + 2;
      middle = n + u / 2;
      vector<string> result = { first_line, second_line };
      result.insert(result.end(), shifted_lines.begin(), shifted_lines.end());
      return result;
  }

  // Only right child
  if (root->left == Node::getNIL()) {
      int m, q, y;
      vector<string> right_lines = display(root->right, m, q, y);
      string first_line = s + string(y, '_') + string(m - y, ' ');
      string second_line = string(u + y, ' ') + '\\' + string(m - y - 1, ' ');

      vector<string> shifted_lines;
      for (const string& line : right_lines)
          shifted_lines.push_back(string(u, ' ') + line);

      width = m + u;
      height = q + 2;
      middle = u / 2;
      vector<string> result = { first_line, second_line };
      result.insert(result.end(), shifted_lines.begin(), shifted_lines.end());
      return result;
  }

  // Both children
  int n, p, x;
  int m, q, y;
  vector<string> left_lines = display(root->left, n, p, x);
  vector<string> right_lines = display(root->right, m, q, y);
  string first_line = string(x + 1, ' ') + string(n - x - 1, '_') + s + string(y, '_') + string(m - y, ' ');
  string second_line = string(x, ' ') + '/' + string(n - x - 1 + u + y, ' ') + '\\' + string(m - y - 1, ' ');

  if (p < q) left_lines.resize(q, string(n, ' '));
  if (q < p) right_lines.resize(p, string(m, ' '));

  vector<string> lines;
  for (size_t i = 0; i < left_lines.size(); ++i)
      lines.push_back(left_lines[i] + string(u, ' ') + right_lines[i]);

  width = n + m + u;
  height = max(p, q) + 2;
  middle = n + u / 2;
  vector<string> result;
  result.push_back(first_line);
  result.push_back(second_line);
  result.insert(result.end(), lines.begin(), lines.end());
  return result;
}

// main func to printing tree
void print_RBT(Node* root) {
    if (root == Node::getNIL()) {
        cout << "(empty tree)" << endl;
        return;
    }

    int width, height, middle;
    vector<string> lines = display(root, width, height, middle);
    for (const string& line : lines)
        cout << line << endl;
}
void ascending_insert(RedBlackTree* tree, int n) {
    for(int i = 1; i <= n; i++) {
        tree->insert(i);
        if (!big_tree) {
            cout << endl;
            cout << "INSERT: " << i << endl;
            print_RBT(tree->root);
            cout << "Height: " << tree->tree_height() << endl;
        }
    }
}

// time-based seed
unsigned seed = chrono::system_clock::now().time_since_epoch().count();

void random_insert(RedBlackTree* tree, int n) {
    vector<int> keys;
    for (int i = 1; i <= n; ++i) {
        keys.push_back(i);
    }
    shuffle(keys.begin(), keys.end(), default_random_engine(seed));

    for (int key : keys) {
        tree->insert(key);
        if (!big_tree) {
            cout << "\nINSERT: " << key << endl;
            print_RBT(tree->root);
            cout << "Height: " << tree->tree_height() << endl;
        }
    }
}
void random_delete(RedBlackTree* tree, int n) {
    std::vector<int> keys;
    for (int i = 1; i <= n; ++i) {
        keys.push_back(i);
    }
    std::shuffle(keys.begin(), keys.end(), default_random_engine(seed));

    for (int key : keys) {
        tree->delete_node(key);
        if (!big_tree) {
            cout << "\nDELETE: " << key << endl;
            print_RBT(tree->root);
            cout << "Height: " << tree->tree_height() << endl;
        }
    }
}

int metrics_cost(vector<int> log) {
    if (log.size() == 0) return 0;
    int sum = accumulate(log.begin(), log.end(), 0);
    return sum / log.size();
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cout << "Wrong number of arguments\n";
        return 1;
    }

    int n;
    try {
        n = stoi(argv[1]);
    } catch (...) {
        cout << "Error: n has to be an integer\n";
        return 1;
    }

    if (n > 30) {
        big_tree = true;
    }

    RedBlackTree rbt;

    auto start = chrono::steady_clock::now();

    cout << "----1 case: ascending_insert and random_delete for n = " << n << "----\n";

    ascending_insert(&rbt, n);

    cout << "Ascending insert average cost comparisons: " << metrics_cost(rbt.insert_comparisons) << "\n";
    cout << "Ascending insert average cost pointer: " << metrics_cost(rbt.insert_pointer_ops) << "\n";
    cout << "Ascending insert average height: " << metrics_cost(rbt.insert_heights) << "\n";

    if (!rbt.insert_comparisons.empty())
        cout << "Ascending insert max comparisons: " << *max_element(rbt.insert_comparisons.begin(), rbt.insert_comparisons.end()) << "\n";
    if (!rbt.insert_pointer_ops.empty())
        cout << "Ascending insert max pointer: " << *max_element(rbt.insert_pointer_ops.begin(), rbt.insert_pointer_ops.end()) << "\n";
    if (!rbt.insert_heights.empty())
        cout << "Ascending insert max height: " << *max_element(rbt.insert_heights.begin(), rbt.insert_heights.end()) << "\n";

    random_delete(&rbt, n);

    cout << "Random delete after ascending insert average cost comparisons: " << metrics_cost(rbt.delete_comparisons) << "\n";
    cout << "Random delete after ascending insert average cost pointer: " << metrics_cost(rbt.delete_pointer_ops) << "\n";
    cout << "Random delete after ascending insert average height: " << metrics_cost(rbt.delete_heights) << "\n";

    if (!rbt.delete_comparisons.empty())
        cout << "Random delete after ascending insert max comparisons: " << *max_element(rbt.delete_comparisons.begin(), rbt.delete_comparisons.end()) << "\n";
    if (!rbt.delete_pointer_ops.empty())
        cout << "Random delete after ascending insert max pointer: " << *max_element(rbt.delete_pointer_ops.begin(), rbt.delete_pointer_ops.end()) << "\n";
    if (!rbt.delete_heights.empty())
        cout << "Random delete after ascending insert max height: " << *max_element(rbt.delete_heights.begin(), rbt.delete_heights.end()) << "\n";

    cout << "\n";

    RedBlackTree rbt2;

    cout << "----2 case: random_insert and random_delete for n = " << n << "----\n";

    random_insert(&rbt2, n);

    cout << "Random insert average cost comparisons: " << metrics_cost(rbt2.insert_comparisons) << "\n";
    cout << "Random insert average cost pointer: " << metrics_cost(rbt2.insert_pointer_ops) << "\n";
    cout << "Random insert average height: " << metrics_cost(rbt2.insert_heights) << "\n";

    if (!rbt2.insert_comparisons.empty())
        cout << "Random insert max comparisons: " << *max_element(rbt2.insert_comparisons.begin(), rbt2.insert_comparisons.end()) << "\n";
    if (!rbt2.insert_pointer_ops.empty())
        cout << "Random insert max pointer: " << *max_element(rbt2.insert_pointer_ops.begin(), rbt2.insert_pointer_ops.end()) << "\n";
    if (!rbt2.insert_heights.empty())
        cout << "Random insert max height: " << *max_element(rbt2.insert_heights.begin(), rbt2.insert_heights.end()) << "\n";

    random_delete(&rbt2, n);

    cout << "Random delete after random insert average cost comparisons: " << metrics_cost(rbt2.delete_comparisons) << "\n";
    cout << "Random delete after random insert average cost pointer: " << metrics_cost(rbt2.delete_pointer_ops) << "\n";
    cout << "Random delete after random insert average height: " << metrics_cost(rbt2.delete_heights) << "\n";

    if (!rbt2.delete_comparisons.empty())
        cout << "Random delete after random insert max comparisons: " << *max_element(rbt2.delete_comparisons.begin(), rbt2.delete_comparisons.end()) << "\n";
    if (!rbt2.delete_pointer_ops.empty())
        cout << "Random delete after random insert max pointer: " << *max_element(rbt2.delete_pointer_ops.begin(), rbt2.delete_pointer_ops.end()) << "\n";
    if (!rbt2.delete_heights.empty())
        cout << "Random delete after random insert max height: " << *max_element(rbt2.delete_heights.begin(), rbt2.delete_heights.end()) << "\n";

    auto end = chrono::steady_clock::now();
    auto elapsed = chrono::duration_cast<chrono::milliseconds>(end - start).count();

    cout << "Time elapsed: " << elapsed / 1000.0 << " seconds\n";

    return 0;
}