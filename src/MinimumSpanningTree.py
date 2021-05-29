import numpy as np
from GraphRepresentation import GraphRepresentation


def minimum_spanning_tree(adjacency_matrix: np.ndarray):
    """Find a minimum spanning tree of a given tree using Prims algorithm and return its adjacency matrix"""
    n = np.size(adjacency_matrix, axis=1)
    T = [0]
    W = [i for i in range(1, n)]

    matrix = np.zeros((n, n), dtype=int)
    v_x = 0
    v_y = 0

    while W:
        min_v = np.inf
        for v in T:
            for u in W:
                if adjacency_matrix[v][u] != 0 and adjacency_matrix[v][u] < min_v:
                    min_v = adjacency_matrix[v][u]
                    v_x = v
                    v_y = u
        T.append(v_y)
        W.remove(v_y)
        matrix[v_x][v_y] = matrix[v_y][v_x] = adjacency_matrix[v_x][v_y]

    return matrix, GraphRepresentation.ADJACENCY_MATRIX
