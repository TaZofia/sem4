from http.server import nobody
from random import randint

import networkx as nx
import numpy as np
import random

from matplotlib import pyplot as plt

m = 1000
T_max = 0.002       # max value, T - it is the average delay in network
p = 0.75



def get_graph():
    G = nx.Graph()

    for i in range(1, 21):
        G.add_node(f'v{i}')     # nodes


    G.add_edges_from([
        ('v1', 'v2'), ('v1', 'v3'), ('v1', 'v4'),
        ('v2', 'v5'), ('v2', 'v6'),
        ('v3', 'v7'), ('v3', 'v8'),
        ('v4', 'v9'),
        ('v5', 'v10'), ('v5', 'v11'),
        ('v6', 'v12'),
        ('v7', 'v13'), ('v7', 'v14'),
        ('v8', 'v15'),
        ('v9', 'v16'),
        ('v10', 'v17'),
        ('v11', 'v18'),
        ('v12', 'v19'),
        ('v13', 'v20'),
        ('v14', 'v16'),
        ('v15', 'v17'),
        ('v16', 'v18'),
        ('v17', 'v19'),
        ('v18', 'v20')
    ])

    return G


def get_N():
    # Generate the matrix of packet intensities N where N[i][j] is the number of packets from node i to node j.
    N = np.array([
        [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1],
        [4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2],
        [5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
        [6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4],
        [7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1],
        [4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2],
        [5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
        [6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4],
        [7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1],
        [4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2],
        [5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
        [6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4]
    ])

    for i in range(20):     # nobody sends a packet itself
        N[i][i] = 0

    return N


def draw_graph(G):
    pos = nx.spring_layout(G)  # Układ wierzchołków
    labels = nx.get_edge_attributes(G, 'a')  # Przepływ na krawędziach
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Network")
    plt.show()


def calculate_a(G, N):
    a = {e: 0 for e in G.edges}

    for i in range(len(N)):
        for j in range(len(N)):
            if i != j and N[i][j] > 0:
                try:
                    # Przyjmujemy najkrótszą ścieżkę jako trasę transmisji
                    path = nx.shortest_path(G, source=("v" + str(i + 1)), target=("v" + str(j + 1)))

                    # Dzielenie ruchu na poszczególne krawędzie ścieżki
                    path_edges = list(zip(path[:-1], path[1:]))
                    for e in path_edges:
                        # Ujednolicamy reprezentację krawędzi (bez względu na kolejność węzłów)
                        e_norm = tuple(sorted(e))
                        if e_norm in a:
                            a[e_norm] += N[i][j]
                except nx.NetworkXNoPath:
                    # Jeśli nie ma ścieżki, pomijamy tę parę
                    continue
    return a

def calculate_c(G):
    return {e: randint(2000, 2200) * m for e in G.edges}

def check_if_viable(G, a, c):
    for e in G.edges:
        if (c.get(e) / m) < a.get(e):
            return False
    return True

def compute_network_delay(G, N, c, a):
    # Calculate total packet intensity
    G_sum = np.sum(N)
    # Compute delay sum using the formula (ensure division is proper)
    delay_sum = sum(a.get(e, 0) / (c.get(e, 1) / m - a.get(e, 0)) for e in G.edges)
    T = (1 / G_sum) * delay_sum
    return T

def estimate_reliability(G, N, c, num_samples=500):
    count = 0
    for _ in range(num_samples):
        G_temp = G.copy()
        for e in list(G.edges):
            if random.random() > p:  # simulate edge failure
                G_temp.remove_edge(*e)
        if nx.is_connected(G_temp):
            a = calculate_a(G, N)
            T = compute_network_delay(G_temp, N, c, a)
            if T < T_max:
                count += 1
    return count / num_samples

def run_experiments():
    G = get_graph()
    N = get_N()
    a = calculate_a(G, N)
    c = calculate_c(G)

    draw_graph(G)

    print("\n--- Eksperymenty dla różnych wartości N: ---\n")
    for scale in [1, 2, 3, 4, 5]:
        print(f'N x {scale}')
        N_scaled = (N * scale).astype(int)
        a_scaled = calculate_a(G, N_scaled)
        viable = check_if_viable(G, a_scaled, c)
        if not viable:
            print("dupadupadupadupa\n")
        else:
            print("Original network delay:", compute_network_delay(G, N, c, a))
            print("New network delay:", compute_network_delay(G, N_scaled, c, a_scaled))
            reliability = estimate_reliability(G, N_scaled, c)
            print(f'Reliability: {reliability}\n')


    print("\n--- Eksperymenty dla różnych wartości c: ---\n")
    for scale in [1, 5, 10, 30]:
        print(f'c x {scale}')
        c_scaled = {e: int(c[e] * scale) for e in G.edges}
        viable = check_if_viable(G, a, c_scaled)
        if not viable:
            print("dupadupadupadupa\n")
        else:
            print("Original network delay:", compute_network_delay(G, N, c, a))
            print("New network delay:", compute_network_delay(G, N, c_scaled, a))
            reliability = estimate_reliability(G, N, c_scaled)
            print(f'Reliability: {reliability}\n')

    print("\n--- Eksperymenty dla różnych topologii: ---\n")
    for extra_edges in [1, 5, 10, 30]:
        print(f'extra edges: {extra_edges}')
        new_edges = []
        for _ in range(extra_edges):
            u, v = ("v" + str(random.randint(1, 20))), ("v" + str(random.randint(1, 20)))
            if u != v:
                new_edges.append((u, v))
        G_extended = G.copy()
        G_extended.add_edges_from(new_edges)
        c_extended = {e: c.get(e, randint(2000, 2200) * m) for e in G_extended.edges}
        a_extended = calculate_a(G_extended, N)

        viable = check_if_viable(G_extended, a_extended, c_extended)
        if not viable:
            print("dupadupadupadupa\n")
        else:
            print("Original network delay:", compute_network_delay(G, N, c, a))
            print("New network delay:", compute_network_delay(G_extended, N, c_extended, a_extended))
            reliability = estimate_reliability(G_extended, N, c_extended)
            print(f'Reliability: {reliability}\n')


if __name__ == "__main__":
    run_experiments()
