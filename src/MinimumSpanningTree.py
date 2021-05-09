import numpy as np
from GraphRepresentation import GraphRepresentation


def minimum_spanning_tree(matrix: np.ndarray):
    """Find a minimum spanning tree of a given tree using Prims algorithm and return its adjacency matrix"""
    original = matrix.astype('float64')
    original[matrix == 0] = np.nan
    n = np.size(original, axis=1)
    T = []
    W = []
    mat = np.zeros((n, n), dtype=int)

    T.append(0)
    original[:, 0] = np.nan

    for i in range(1, n):
        W.append(i)

    while W:
        mask = np.zeros(original.shape, dtype=np.bool)
        mask[T] = True
        min_weight = np.nanargmin(original[mask])
        i = min_weight // n
        j = min_weight % n
        T.append(j)
        W.remove(j)
        original[:, j] = np.nan
        mat[i][j] = matrix[i][j]

    return mat, GraphRepresentation.ADJACENCY_MATRIX

