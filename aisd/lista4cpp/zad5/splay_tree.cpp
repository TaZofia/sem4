#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <random>
#include <chrono>
#include <numeric>
#include <cstdlib>

using namespace std;
enum Operation {INSERT, DELETE};

bool big_tree = false;

class Node {
public:
    int value;
    Node* left;
    Node* right;
    Node* parent;
    int height;

    // normal constructor
    Node(int val)
        : value(val), left(getNIL()), right(getNIL()), parent(getNIL()), height(1) {}

    // constructor for NIL
    Node(int val, bool is_nil)
      : value(val), left(nullptr), right(nullptr), parent(nullptr), height(0) {}

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
};

class SplayTree {
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

    SplayTree() {
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

    Node* rotate_right(Node* pivot) {
        Node* new_root = pivot->left;
        pivot->left = new_root->right;
        new_root->right = pivot;
        current_pointer_ops += 4;

        update_height(pivot);
        update_height(new_root);

        return new_root;
    }

    Node* rotate_left(Node* pivot) {
        Node* new_root = pivot->right;
        pivot->right = new_root->left;
        new_root->left = pivot;
        current_pointer_ops += 4;

        update_height(pivot);
        update_height(new_root);

        return new_root;
    }

    Node* splay(Node* node, int value) {
        if (node == Node::getNIL())
            return node;

        current_comparisons++;
        if (node->value == value) {
            return node;
        }
        current_comparisons++;
        if (value < node->value) {
            current_pointer_ops++;
            if (node->left == Node::getNIL()) {
                return node;
            }
            current_comparisons++;
            current_pointer_ops++;

            if (value < node->left->value) {
                // Zig-Zig (Left Left)
                node->left->left = splay(node->left->left, value);
                node = rotate_right(node);
                update_height(node);
                current_pointer_ops += 4;
            }
            else if (value > node->left->value) {
                // Zig-Zag (Left Right)
                current_pointer_ops++;
                current_comparisons++;
                node->left->right = splay(node->left->right, value);
                current_pointer_ops += 6;
                if (node->left->right != Node::getNIL()) {
                    node->left = rotate_left(node->left);
                    update_height(node->left);
                    current_pointer_ops += 2;
                }
            } else {
                current_comparisons++;
            }

            current_pointer_ops++;
            return (node->left == Node::getNIL()) ? node : rotate_right(node);
        }
        else {
            current_pointer_ops++;
            if (node->right == Node::getNIL()) {
                return node;
            }
            current_comparisons++;
            current_pointer_ops++;

            if (value > node->right->value) {
                // Zag-Zag (Right Right)
                node->right->right = splay(node->right->right, value);
                node = rotate_left(node);
                update_height(node);
                current_pointer_ops += 4;
            }
            else if (value < node->right->value) {
                // Zag-Zig (Right Left)
                current_comparisons++;
                current_pointer_ops++;
                node->right->left = splay(node->right->left, value);
                current_pointer_ops += 6;
                if (node->right->left != Node::getNIL()) {
                    node->right = rotate_right(node->right);
                    update_height(node->right);
                    current_pointer_ops += 2;
                }
            } else {
                current_comparisons++;
            }
            current_pointer_ops++;
            return (node->right == Node::getNIL()) ? node : rotate_left(node);
        }
        update_height_upwards(node);
    }

    void insert(int value) {
        reset_counters();

        current_pointer_ops++;
        if (root == Node::getNIL()) {
            root = new Node(value);
            current_pointer_ops++;
            return;
        }

        root = splay(root, value);
        current_pointer_ops += 2;

        current_comparisons++;
        current_pointer_ops++;
        if (root->value == value) {
            return; // Already in the tree
        }

        Node* new_node = new Node(value);
        current_comparisons++;
        current_pointer_ops++;

        if (value < root->value) {
            new_node->right = root;
            new_node->left = root->left;
            root->left = Node::getNIL();
            update_height_upwards(root);
            current_pointer_ops += 7;
        } else {
            new_node->left = root;
            new_node->right = root->right;
            root->right = Node::getNIL();
            update_height_upwards(root);
            current_pointer_ops += 7;
        }

        root = new_node;
        current_pointer_ops++;
        update_height_upwards(root);
        log_operation(INSERT);
    }

    bool search(int value) {
        root = splay(root, value);
        current_pointer_ops += 2;

        current_pointer_ops++;
        if (root != Node::getNIL()) {
            current_comparisons++;
            current_pointer_ops++;
            return root->value == value;
        } else {
            return false;
        }
    }

    void delete_node(int value) {
        reset_counters();
        current_pointer_ops++;

        if (root == Node::getNIL()) {
            return;
        }

        root = splay(root, value);
        current_pointer_ops += 2;

        current_comparisons++;
        current_pointer_ops++;
        if (root->value != value) {
            return; // Not found
        }

        current_pointer_ops += 2;
        if (root->left == Node::getNIL()) {
            Node* temp = root;
            root = root->right;
            delete temp;
            current_pointer_ops += 3;
            if (root != Node::getNIL()) {
                update_height_upwards(root);
            }
        } else {
            Node* temp = splay(root->left, value);
            temp->right = root->right;
            delete root;
            root = temp;
            current_pointer_ops += 6;
            if (temp->right != Node::getNIL()) {
                update_height_upwards(temp->right);
            }
            update_height_upwards(temp);
        }
        log_operation(DELETE);
    }
};

string to_string_node(Node* node) {
    if (node == Node::getNIL()) return "NIL";
    stringstream ss;
    ss << node->value;
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
  int u = s.length();

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
void print_Splay_Tree(Node* root) {
    if (root == Node::getNIL()) {
        cout << "(empty tree)" << endl;
        return;
    }

    int width, height, middle;
    vector<string> lines = display(root, width, height, middle);
    for (const string& line : lines)
        cout << line << endl;
}

void ascending_insert(SplayTree* tree, int n) {
    for(int i = 1; i <= n; i++) {
        tree->insert(i);
        if (!big_tree) {
            cout << endl;
            cout << "INSERT: " << i << endl;
            print_Splay_Tree(tree->root);
            cout << "Height: " << tree->tree_height() << endl;
        }
    }
}

// time-based seed
unsigned seed = chrono::system_clock::now().time_since_epoch().count();

void random_insert(SplayTree* tree, int n) {
    vector<int> keys;
    for (int i = 1; i <= n; ++i) {
        keys.push_back(i);
    }
    shuffle(keys.begin(), keys.end(), default_random_engine(seed));

    for (int key : keys) {
        tree->insert(key);
        if (!big_tree) {
            cout << "\nINSERT: " << key << endl;
            print_Splay_Tree(tree->root);
            cout << "Height: " << tree->tree_height() << endl;
        }
    }
}
void random_delete(SplayTree* tree, int n) {
    std::vector<int> keys;
    for (int i = 1; i <= n; ++i) {
        keys.push_back(i);
    }
    std::shuffle(keys.begin(), keys.end(), default_random_engine(seed));

    for (int key : keys) {
        tree->delete_node(key);
        if (!big_tree) {
            cout << "\nDELETE: " << key << endl;
            print_Splay_Tree(tree->root);
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

    SplayTree splay1;

    auto start = chrono::steady_clock::now();

    cout << "----1 case: ascending_insert and random_delete for n = " << n << "----\n";

    ascending_insert(&splay1, n);

    cout << "Ascending insert average cost comparisons: " << metrics_cost(splay1.insert_comparisons) << "\n";
    cout << "Ascending insert average cost pointer: " << metrics_cost(splay1.insert_pointer_ops) << "\n";
    cout << "Ascending insert average height: " << metrics_cost(splay1.insert_heights) << "\n";

    if (!splay1.insert_comparisons.empty())
        cout << "Ascending insert max comparisons: " << *max_element(splay1.insert_comparisons.begin(), splay1.insert_comparisons.end()) << "\n";
    if (!splay1.insert_pointer_ops.empty())
        cout << "Ascending insert max pointer: " << *max_element(splay1.insert_pointer_ops.begin(), splay1.insert_pointer_ops.end()) << "\n";
    if (!splay1.insert_heights.empty())
        cout << "Ascending insert max height: " << *max_element(splay1.insert_heights.begin(), splay1.insert_heights.end()) << "\n";

    random_delete(&splay1, n);

    cout << "Random delete after ascending insert average cost comparisons: " << metrics_cost(splay1.delete_comparisons) << "\n";
    cout << "Random delete after ascending insert average cost pointer: " << metrics_cost(splay1.delete_pointer_ops) << "\n";
    cout << "Random delete after ascending insert average height: " << metrics_cost(splay1.delete_heights) << "\n";

    if (!splay1.delete_comparisons.empty())
        cout << "Random delete after ascending insert max comparisons: " << *max_element(splay1.delete_comparisons.begin(), splay1.delete_comparisons.end()) << "\n";
    if (!splay1.delete_pointer_ops.empty())
        cout << "Random delete after ascending insert max pointer: " << *max_element(splay1.delete_pointer_ops.begin(), splay1.delete_pointer_ops.end()) << "\n";
    if (!splay1.delete_heights.empty())
        cout << "Random delete after ascending insert max height: " << *max_element(splay1.delete_heights.begin(), splay1.delete_heights.end()) << "\n";

    cout << "\n";

    SplayTree splay2;

    cout << "----2 case: random_insert and random_delete for n = " << n << "----\n";

    random_insert(&splay2, n);

    cout << "Random insert average cost comparisons: " << metrics_cost(splay2.insert_comparisons) << "\n";
    cout << "Random insert average cost pointer: " << metrics_cost(splay2.insert_pointer_ops) << "\n";
    cout << "Random insert average height: " << metrics_cost(splay2.insert_heights) << "\n";

    if (!splay2.insert_comparisons.empty())
        cout << "Random insert max comparisons: " << *max_element(splay2.insert_comparisons.begin(), splay2.insert_comparisons.end()) << "\n";
    if (!splay2.insert_pointer_ops.empty())
        cout << "Random insert max pointer: " << *max_element(splay2.insert_pointer_ops.begin(), splay2.insert_pointer_ops.end()) << "\n";
    if (!splay2.insert_heights.empty())
        cout << "Random insert max height: " << *max_element(splay2.insert_heights.begin(), splay2.insert_heights.end()) << "\n";

    random_delete(&splay2, n);

    cout << "Random delete after random insert average cost comparisons: " << metrics_cost(splay2.delete_comparisons) << "\n";
    cout << "Random delete after random insert average cost pointer: " << metrics_cost(splay2.delete_pointer_ops) << "\n";
    cout << "Random delete after random insert average height: " << metrics_cost(splay2.delete_heights) << "\n";

    if (!splay2.delete_comparisons.empty())
        cout << "Random delete after random insert max comparisons: " << *max_element(splay2.delete_comparisons.begin(), splay2.delete_comparisons.end()) << "\n";
    if (!splay2.delete_pointer_ops.empty())
        cout << "Random delete after random insert max pointer: " << *max_element(splay2.delete_pointer_ops.begin(), splay2.delete_pointer_ops.end()) << "\n";
    if (!splay2.delete_heights.empty())
        cout << "Random delete after random insert max height: " << *max_element(splay2.delete_heights.begin(), splay2.delete_heights.end()) << "\n";

    auto end = chrono::steady_clock::now();
    auto elapsed = chrono::duration_cast<chrono::milliseconds>(end - start).count();

    cout << "Time elapsed: " << elapsed / 1000.0 << " seconds\n";

    return 0;
}