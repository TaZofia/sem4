import networkx as nx
import matplotlib.pyplot as plt
import random
from zad1 import prim_mst
from zad1 import generate_graph

# build tree as a graph
def build_tree(edges):
    T = nx.Graph()
    for u, v, _ in edges:
        T.add_edge(u, v)
    return T

def compute_schedule(tree, root):
    """Zwraca: (rundy_dla_każdego_węzła, kolejność_dzieci_dla_każdego_węzła)"""
    rounds = {}
    schedule = {}

    def dfs(node, parent):
        children = [child for child in tree.neighbors(node) if child != parent]
        children_info = []
        for child in children:
            dfs(child, node)
            children_info.append((rounds[child], child))
        # Sortuj dzieci po potrzebnych rundach malejąco
        children_info.sort(reverse=True)
        schedule[node] = [child for _, child in children_info]
        # Oblicz liczbę rund dla tego wierzchołka
        max_time = 0
        for i, (_, child) in enumerate(children_info):
            max_time = max(max_time, i + 1 + rounds[child])
        rounds[node] = max_time

    dfs(root, None)
    return rounds, schedule

def experiment_propagation(n_min, n_max, step, rep):
    avg_rounds, max_rounds, min_rounds = [], [], []
    sizes = list(range(n_min, n_max + 1, step))

    for n in sizes:
        round_counts = []
        for _ in range(rep):
            G = generate_graph(n)                       # graph
            _, mst_edges = prim_mst(G)                  # MST
            T = build_tree(mst_edges)                   # building a graph
            root = random.choice(list(T.nodes))         # we choose random root
            rounds, _ = compute_schedule(T, root)
            round_counts.append(rounds[root])           # save numbr of rounds from root
        avg_rounds.append(sum(round_counts) / rep)
        max_rounds.append(max(round_counts))
        min_rounds.append(min(round_counts))
    return sizes, avg_rounds, max_rounds, min_rounds

def plot_propagation_results(sizes, avg_rounds, max_rounds, min_rounds):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, avg_rounds, label='Średnia liczba rund', marker='o')
    plt.plot(sizes, max_rounds, label='Maksymalna liczba rund', marker='s')
    plt.plot(sizes, min_rounds, label='Minimalna liczba rund', marker='^')
    plt.xlabel('Liczba wierzchołków')
    plt.ylabel('Liczba rund do rozesłania informacji')
    plt.title('Analiza średniego przypadku propagacji informacji w drzewie')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('./num_of_min_rounds.png')


n_min, n_max, step, rep = 10, 200, 10, 20
sizes, avg_rounds, max_rounds, min_rounds = experiment_propagation(n_min, n_max, step, rep)
plot_propagation_results(sizes, avg_rounds, max_rounds, min_rounds)
