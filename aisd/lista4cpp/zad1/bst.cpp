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

class BinarySearchTree {
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

  BinarySearchTree() {
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

    Node* search(Node* node, int key) {
      while (node != Node::getNIL()) {
        current_comparisons++;
        if (key == node->value) {
          return node;
        }
        current_comparisons++;
        current_pointer_ops++;
        if (key < node->value) {
          node = node->left;
        } else {
          node = node->right;
        }
      }
      return Node::getNIL();
    }

  void insert_node(Node* z) {
    reset_counters();

    Node* y = Node::getNIL();
    Node* x = root;
    current_pointer_ops++;

    while (x != Node::getNIL()) {
      y = x;
      current_comparisons++;
      current_pointer_ops++;
      if (z->value < x->value) {
        x = x->left;
      } else {
        x = x->right;
      }
    }
    z->parent = y;
    current_pointer_ops++;

    if (y == Node::getNIL()) {
      root = z;              // tree was empty
      current_pointer_ops++;
    } else if (z->value < y->value) {
      y->left = z;
      current_pointer_ops++;
      current_comparisons++;
    } else {
      y->right = z;
      current_pointer_ops++;
      current_comparisons++;
    }

    // go up and update heights in nodes
    update_height_upwards(z->parent);

    log_operation(INSERT);
  }

  void transplant(Node* u, Node* v) {
    current_pointer_ops++;
    if (u->parent == Node::getNIL()) {
      root = v;
      current_pointer_ops++;
    }
    else if (u == u->parent->left) {
      u->parent->left = v;
      current_pointer_ops += 4;
    }
    else {
      u->parent->right = v;
      current_pointer_ops += 4;
    }

    if (v != Node::getNIL()) {
      v->parent = u->parent;
      current_pointer_ops += 2;
    }
  }

  Node* tree_minimum(Node* x) {
    while (x->left != Node::getNIL()) {
      x = x->left;
      current_pointer_ops += 2;
    }
    return x;
  }

  Node* tree_maximum(Node* x) {
    while (x->right != Node::getNIL()) {
      x = x->right;
      current_pointer_ops += 2;
    }
    return x;
  }

  void delete_node(int val_to_delete) {
    reset_counters();

    Node* z = search(root, val_to_delete);    // node which we found

    Node* update_start = Node::getNIL();

    current_pointer_ops++;
    if (z->left == Node::getNIL()) {
      update_start = z->parent;
      transplant(z, z->right);
      current_pointer_ops++;
    } else if (z->right == Node::getNIL()) {
      update_start = z->parent;
      transplant(z, z->left);
      current_pointer_ops += 2;
    } else {
      Node* y = tree_minimum(z->right);
      current_pointer_ops += 2;

      update_start = y;

      current_pointer_ops++;
      if (y->parent != z) {
        transplant(y, y->right);
        y->right = z->right;
        current_pointer_ops += 4;
        if (y->right != Node::getNIL()) {
          y->right->parent = y;
          current_pointer_ops += 2;
        }
      }
      transplant(z, y);
      y->left = z->left;
      current_pointer_ops += 3;
      if (y->left != Node::getNIL()) {
        y->left->parent = y;
        current_pointer_ops += 2;
      }
    }
    update_height_upwards(update_start);
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
void print_BST(Node* root) {
    if (root == Node::getNIL()) {
        cout << "(empty tree)" << endl;
        return;
    }

    int width, height, middle;
    vector<string> lines = display(root, width, height, middle);
    for (const string& line : lines)
        cout << line << endl;
}

void ascending_insert(BinarySearchTree* tree, int n) {
  for(int i = 1; i <= n; i++) {
    Node* node_to_insert = new Node(i);
    tree->insert_node(node_to_insert);
    if (!big_tree) {
      cout << endl;
      cout << "INSERT: " << i << endl;
      print_BST(tree->root);
      cout << "Height: " << tree->tree_height() << endl;
    }
  }
}

// time-based seed
unsigned seed = chrono::system_clock::now().time_since_epoch().count();

void random_insert(BinarySearchTree* tree, int n) {
  vector<int> keys;
  for (int i = 1; i <= n; ++i) {
    keys.push_back(i);
  }
  shuffle(keys.begin(), keys.end(), default_random_engine(seed));

  for (int key : keys) {
    Node* node_to_insert = new Node(key);
    tree->insert_node(node_to_insert);
    if (!big_tree) {
      cout << "\nINSERT: " << key << endl;
      print_BST(tree->root);
      cout << "Height: " << tree->tree_height() << endl;
    }
  }
}
void random_delete(BinarySearchTree* tree, int n) {
  std::vector<int> keys;
  for (int i = 1; i <= n; ++i) {
    keys.push_back(i);
  }
  std::shuffle(keys.begin(), keys.end(), default_random_engine(seed));

  for (int key : keys) {
    tree->delete_node(key);
    if (!big_tree) {
      cout << "\nDELETE: " << key << endl;
      print_BST(tree->root);
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

    BinarySearchTree bst;

    auto start = chrono::steady_clock::now();

    cout << "----1 case: ascending_insert and random_delete for n = " << n << "----\n";

    ascending_insert(&bst, n);

    cout << "Ascending insert average cost comparisons: " << metrics_cost(bst.insert_comparisons) << "\n";
    cout << "Ascending insert average cost pointer: " << metrics_cost(bst.insert_pointer_ops) << "\n";
    cout << "Ascending insert average height: " << metrics_cost(bst.insert_heights) << "\n";

    if (!bst.insert_comparisons.empty())
        cout << "Ascending insert max comparisons: " << *max_element(bst.insert_comparisons.begin(), bst.insert_comparisons.end()) << "\n";
    if (!bst.insert_pointer_ops.empty())
        cout << "Ascending insert max pointer: " << *max_element(bst.insert_pointer_ops.begin(), bst.insert_pointer_ops.end()) << "\n";
    if (!bst.insert_heights.empty())
        cout << "Ascending insert max height: " << *max_element(bst.insert_heights.begin(), bst.insert_heights.end()) << "\n";

    random_delete(&bst, n);

    cout << "Random delete after ascending insert average cost comparisons: " << metrics_cost(bst.delete_comparisons) << "\n";
    cout << "Random delete after ascending insert average cost pointer: " << metrics_cost(bst.delete_pointer_ops) << "\n";
    cout << "Random delete after ascending insert average height: " << metrics_cost(bst.delete_heights) << "\n";

    if (!bst.delete_comparisons.empty())
        cout << "Random delete after ascending insert max comparisons: " << *max_element(bst.delete_comparisons.begin(), bst.delete_comparisons.end()) << "\n";
    if (!bst.delete_pointer_ops.empty())
        cout << "Random delete after ascending insert max pointer: " << *max_element(bst.delete_pointer_ops.begin(), bst.delete_pointer_ops.end()) << "\n";
    if (!bst.delete_heights.empty())
        cout << "Random delete after ascending insert max height: " << *max_element(bst.delete_heights.begin(), bst.delete_heights.end()) << "\n";

    cout << "\n";

    BinarySearchTree bst2;

    cout << "----2 case: random_insert and random_delete for n = " << n << "----\n";

    random_insert(&bst2, n);

    cout << "Random insert average cost comparisons: " << metrics_cost(bst2.insert_comparisons) << "\n";
    cout << "Random insert average cost pointer: " << metrics_cost(bst2.insert_pointer_ops) << "\n";
    cout << "Random insert average height: " << metrics_cost(bst2.insert_heights) << "\n";

    if (!bst2.insert_comparisons.empty())
        cout << "Random insert max comparisons: " << *max_element(bst2.insert_comparisons.begin(), bst2.insert_comparisons.end()) << "\n";
    if (!bst2.insert_pointer_ops.empty())
        cout << "Random insert max pointer: " << *max_element(bst2.insert_pointer_ops.begin(), bst2.insert_pointer_ops.end()) << "\n";
    if (!bst2.insert_heights.empty())
        cout << "Random insert max height: " << *max_element(bst2.insert_heights.begin(), bst2.insert_heights.end()) << "\n";

    random_delete(&bst2, n);

    cout << "Random delete after random insert average cost comparisons: " << metrics_cost(bst2.delete_comparisons) << "\n";
    cout << "Random delete after random insert average cost pointer: " << metrics_cost(bst2.delete_pointer_ops) << "\n";
    cout << "Random delete after random insert average height: " << metrics_cost(bst2.delete_heights) << "\n";

    if (!bst2.delete_comparisons.empty())
        cout << "Random delete after random insert max comparisons: " << *max_element(bst2.delete_comparisons.begin(), bst2.delete_comparisons.end()) << "\n";
    if (!bst2.delete_pointer_ops.empty())
        cout << "Random delete after random insert max pointer: " << *max_element(bst2.delete_pointer_ops.begin(), bst2.delete_pointer_ops.end()) << "\n";
    if (!bst2.delete_heights.empty())
        cout << "Random delete after random insert max height: " << *max_element(bst2.delete_heights.begin(), bst2.delete_heights.end()) << "\n";

    auto end = chrono::steady_clock::now();
    auto elapsed = chrono::duration_cast<chrono::milliseconds>(end - start).count();

    cout << "Time elapsed: " << elapsed / 1000.0 << " seconds\n";

    return 0;
}

