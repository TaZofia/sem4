import random
import matplotlib.pyplot as plt
import numpy as np

class BinomialHeapNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None

class BinomialHeap:
    def __init__(self):
        self.head = None
        # Comparison counter for the current operation
        self.comparisons = 0

    def reset_comparisons(self):
        self.comparisons = 0

    def link(self, y, z):
        # Make y a child of z
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def merge_root_lists(self, h1, h2):
        # Merge two root lists by ascending order of degree
        if h1 is None:
            return h2
        if h2 is None:
            return h1
        head = None
        tail = None
        p1 = h1
        p2 = h2
        while p1 and p2:
            # Count comparison of degrees
            self.comparisons += 1
            if p1.degree <= p2.degree:
                if head is None:
                    head = p1
                    tail = p1
                else:
                    tail.sibling = p1
                    tail = p1
                p1 = p1.sibling
            else:
                if head is None:
                    head = p2
                    tail = p2
                else:
                    tail.sibling = p2
                    tail = p2
                p2 = p2.sibling
        # Append rest
        tail_next = p1 if p1 else p2
        if tail:
            tail.sibling = tail_next
        else:
            head = tail_next
        return head

    def union(self, other):
        # Union of two heaps returns a new heap with merged root lists and consolidated trees
        new_heap = BinomialHeap()
        new_heap.head = self.merge_root_lists(self.head, other.head)
        if new_heap.head is None:
            return new_heap

        prev_x = None
        x = new_heap.head
        next_x = x.sibling

        while next_x is not None:
            # Compare degrees to decide merge
            new_heap.comparisons += 1
            if x.degree != next_x.degree or \
               (next_x.sibling is not None and next_x.sibling.degree == x.degree):
                prev_x = x
                x = next_x
            else:
                # x.degree == next_x.degree, merge these two trees
                new_heap.comparisons += 1
                if x.key <= next_x.key:
                    x.sibling = next_x.sibling
                    self.link(next_x, x)
                else:
                    if prev_x is None:
                        new_heap.head = next_x
                    else:
                        prev_x.sibling = next_x
                    self.link(x, next_x)
                    x = next_x
                # no change to prev_x here
            next_x = x.sibling
        return new_heap

    def insert(self, key):
        # Insert by creating a heap with single node and union
        node = BinomialHeapNode(key)
        new_heap = BinomialHeap()
        new_heap.head = node
        # Union current heap with new heap, counting comparisons accordingly
        union_heap = self.union(new_heap)
        self.head = union_heap.head
        # Add comparisons done in union
        self.comparisons += union_heap.comparisons

    def extract_min(self):
        if self.head is None:
            return None

        # Find min root and keep track of previous
        prev_min = None
        min_node = self.head
        prev = None
        curr = self.head
        # Reset comparisons for this operation
        self.reset_comparisons()

        while curr is not None:
            self.comparisons += 1
            if curr.key < min_node.key:
                min_node = curr
                prev_min = prev
            prev = curr
            curr = curr.sibling

        # Remove min_node from root list
        if prev_min is None:
            self.head = min_node.sibling
        else:
            prev_min.sibling = min_node.sibling

        # Reverse min_node's children and create new heap
        child = min_node.child
        prev_child = None
        while child:
            next_child = child.sibling
            child.sibling = prev_child
            child.parent = None
            prev_child = child
            child = next_child
        new_heap = BinomialHeap()
        new_heap.head = prev_child

        # Union new heap with current heap
        union_heap = self.union(new_heap)
        self.head = union_heap.head

        # Add comparisons done in union + during find-min
        self.comparisons += union_heap.comparisons

        return min_node.key, self.comparisons

    def is_empty(self):
        return self.head is None

def run_single_experiment(n, seed=None):
    if seed is not None:
        random.seed(seed)

    # 1. Create two empty heaps H1, H2
    H1 = BinomialHeap()
    H2 = BinomialHeap()

    # 2. Insert n random elements into each heap
    seq1 = [random.randint(1, 10**9) for _ in range(n)]
    seq2 = [random.randint(1, 10**9) for _ in range(n)]

    comparisons_per_insert_H1 = []
    for x in seq1:
        H1.reset_comparisons()
        H1.insert(x)
        comparisons_per_insert_H1.append(H1.comparisons)

    comparisons_per_insert_H2 = []
    for x in seq2:
        H2.reset_comparisons()
        H2.insert(x)
        comparisons_per_insert_H2.append(H2.comparisons)

    # 3. Union the two heaps into H
    H = H1.union(H2)
    comparisons_union = H.comparisons

    # 4. Extract-min 2n times, track comparisons and sorted order check
    extracted = []
    comparisons_extract = []
    prev = -float('inf')
    for _ in range(2*n):
        key, comps = H.extract_min()
        extracted.append(key)
        comparisons_extract.append(comps)
        # Check sorted order incrementally
        assert key >= prev, "Extracted sequence is not sorted!"
        prev = key

    # After all extracts heap should be empty
    assert H.is_empty(), "Heap not empty after extracting all elements!"

    return {
        "insert1": comparisons_per_insert_H1,
        "insert2": comparisons_per_insert_H2,
        "union": comparisons_union,
        "extract": comparisons_extract,
        "extracted_sequence": extracted,
    }

def plot_experiment_cmp():
    n = 200
    repetitions = 5
    step = 10

    plt.figure(figsize=(12, 8))
    for i in range(repetitions):
        result = run_single_experiment(n, seed=i)
        comparisons = result["extract"]
        comparisons_sampled = comparisons[::step]
        plt.plot(range(0, len(comparisons), step), comparisons_sampled, label=f"Run {i+1}")

    plt.title(f"Binomial Heap Extract-Min Comparisons per Operation (n={n}, 5 runs)")
    plt.xlabel("Extract-Min Operation Index")
    plt.ylabel("Number of Comparisons")
    plt.legend()
    plt.grid(True)
    plt.savefig('./zad3_cpm_per_operation.png')

def plot_average_comparisons_vs_n():
    ns = list(range(100, 10001, 100))
    avg_cost_per_element = []

    for n in ns:
        # Run experiment once per n for performance
        result = run_single_experiment(n, seed=42)

        total_comparisons = (
            sum(result["insert1"]) +
            sum(result["insert2"]) +
            result["union"] +
            sum(result["extract"])
        )

        # Divide total comparisons by n (number of elements inserted per heap)
        avg_cost = total_comparisons / n
        avg_cost_per_element.append(avg_cost)

    plt.figure(figsize=(12, 6))
    plt.plot(ns, avg_cost_per_element, marker='o')
    plt.title("Average Comparisons per Element vs n (Binomial Heap)")
    plt.xlabel("n (number of elements inserted per heap)")
    plt.ylabel("Average Comparisons per Element")
    plt.grid(True)
    plt.savefig("./zad3_avg_cpm_per_element.png")

if __name__ == "__main__":
    plot_experiment_cmp()

    # Run and plot average comparisons per operation for n from 100 to 10000
    #plot_average_comparisons_vs_n()
