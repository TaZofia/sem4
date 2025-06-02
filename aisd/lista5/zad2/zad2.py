from collections import defaultdict
import random
import matplotlib.pyplot as plt
import networkx as nx

def compute_propagation_order(tree, root):
    order = {}
    propagation_time = {}

    def dfs(node):
        children = [child for child in tree[node] if child != parent[node]]
        for child in children:
            parent[child] = node
            dfs(child)

        # Sort children by their subtree propagation time
        children.sort(key=lambda x: propagation_time[x], reverse=True)
        order[node] = children

        # Calculate time to inform all descendants
        times = [propagation_time[child] + i + 1 for i, child in enumerate(children)]
        propagation_time[node] = max(times, default=0)

    parent = {root: None}
    dfs(root)
    return order, propagation_time[root]

