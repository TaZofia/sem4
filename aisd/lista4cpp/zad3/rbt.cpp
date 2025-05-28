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

};



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

    RedBlackTree bst;

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