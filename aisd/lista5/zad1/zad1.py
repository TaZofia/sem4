import networkx as nx
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from heapq import heappop, heappush

def generate_graph(n):
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            weight = random.uniform(0, 1)
            G.add_edge(i, j, weight=weight)
    return G

def prim_mst(graph):
    n = len(graph.nodes)
    visited = [False] * n
    min_heap = [(0, 0)]  # (weight, node)
    total_weight = 0

    while min_heap:
        weight, u = heappop(min_heap)       # edge with the lowest weight
        if visited[u]:
            continue
        visited[u] = True
        total_weight += weight
        for v in graph.neighbors(u):
            if not visited[v]:
                heappush(min_heap, (graph[u][v]['weight'], v))
    return total_weight

def kruskal_mst(graph):
    parent = {}
    def find(x):            # helps to know if two vertices are already connected
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x, y):
        rootX, rootY = find(x), find(y)
        if rootX != rootY:
            parent[rootY] = rootX       # trying to connect two sets
            return True         # connect
        return False            # already connected

    for node in graph.nodes:
        parent[node] = node

    edges = sorted(graph.edges(data=True), key=lambda x: x[2]['weight'])
    total_weight = 0
    for u, v, data in edges:
        if union(u, v):
            total_weight += data['weight']
    return total_weight

def run_experiment(n_min, n_max, step, rep):
    prim_times = []
    kruskal_times = []
    sizes = list(range(n_min, n_max + 1, step))

    for n in sizes:
        prim_total, kruskal_total = 0, 0
        for _ in range(rep):
            G = generate_graph(n)

            t0 = time.perf_counter()
            prim_mst(G)
            t1 = time.perf_counter()
            prim_total += (t1 - t0)

            t0 = time.perf_counter()
            kruskal_mst(G)
            t1 = time.perf_counter()
            kruskal_total += (t1 - t0)

        prim_times.append(prim_total / rep)
        kruskal_times.append(kruskal_total / rep)

    return sizes, prim_times, kruskal_times

def plot_results(sizes, prim_times, kruskal_times):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, prim_times, label='Prim\'s Algorithm', marker='o')
    plt.plot(sizes, kruskal_times, label='Kruskal\'s Algorithm', marker='s')
    plt.xlabel('Number of vertices (n)')
    plt.ylabel('Average execution time (s)')
    plt.title('MST Algorithms: Prim vs Kruskal')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('./mst.png')

n_min, n_max, step, rep = 10, 200, 10, 20

sizes, prim_times, kruskal_times = run_experiment(n_min, n_max, step, rep)

plot_results(sizes, prim_times, kruskal_times)
