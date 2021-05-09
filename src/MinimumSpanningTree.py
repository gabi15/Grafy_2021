import numpy as np
from GraphRepresentation import GraphRepresentation


def minimum_spanning_tree(matrix: np.ndarray):
    """Find a minimum spanning tree of a given tree using Prims algorithm and return its adjacency matrix"""
    copy = matrix.astype('float64')
    copy[matrix == 0] = np.nan
    n = np.size(copy, axis=1)
    T = []
    mat = np.zeros(matrix.shape, dtype=int)

    T.append(0)
    copy[:, 0] = np.nan
    W = [i for i in range(1, n)]

    while W:
        mask = np.zeros(matrix.shape, dtype=np.bool)
        mask[T] = True
        min_weight = np.nanargmin(copy[mask])
        i = min_weight // n
        j = min_weight % n
        T.append(j)
        W.remove(j)
        copy[:, j] = np.nan
        mat[i][j] = matrix[i][j]

    return mat, GraphRepresentation.ADJACENCY_MATRIX
