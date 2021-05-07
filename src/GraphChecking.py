from typing import Union

import numpy as np

class BadStartNode(Exception):
    """Raised when the starting node is less than 0 or more than the number of vertices"""

    def  __str__(self):
        return "The starting node is less than 0 or more than the number of vertices"


def is_hamiltonian(matrix: np.ndarray, path: list, visited: list, n: int) -> list:
    """Check if adjacency matrix represents a hamiltonian graph"""
    if len(path) == n:
        if matrix[path[0]][path[-1]] == 1:
            return path
        else:
            visited[path.pop()] = False
            is_hamiltonian(matrix, path, visited, n)

    for i in range(n):
        if matrix[i][path[-1]] == 1 and not visited[i]:
            visited[i] = True
            path.append(i)
            is_hamiltonian(matrix, path, visited, n)
            if len(path) is not n:
                visited[path.pop()] = False


def hamiltonian(matrix: np.ndarray, start: int = 1) -> Union[tuple[bool, list[int]], tuple[bool, None]]:
    """Start the process of checking if the adjacency matrix represents a hamiltonian graph
    starting from the given node """
    n = np.size(matrix, axis=1)

    if start > n or start < 0:
        raise BadStartNode

    path = []
    visited = [False for i in range(n)]
    path.append(start - 1)
    visited[start - 1] = True
    is_hamiltonian(matrix, path, visited, n)
    return (True, path) if len(path) == n else (False, None)
