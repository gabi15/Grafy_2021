import numpy as np

class BadMatrix(Exception):
    """Raised when matrix is empty """

class HamiltonianGraph:

    @staticmethod
    def is_hamiltonian(matrix, path, visited, n):
        """Check if adjacency matrix represents a hamiltonian graph"""
        if len(path)==n:
            if matrix[path[0]][path[-1]] == 1:
                return path
            else:
                visited[path.pop()] = False
                HamiltonianGraph.is_hamiltonian(matrix, path, visited, n)

        for i in range(n):
            if matrix[i][path[-1]]==1 and not visited[i]:
                visited[i] = True
                path.append(i)
                HamiltonianGraph.is_hamiltonian(matrix, path, visited, n)
                if len(path) is not n:
                    visited[path.pop()] = False

    @staticmethod
    def hamiltonian(matrix, start=0):
        """Start the process of checking if the adjacency matrix represents a hamiltonian graph starting from the given node"""
        n = np.size(matrix, axis = 1)

        if n < 1:
            raise BadMatrix

        path = []
        visited = [False for i in range(n)]
        path.append(start)
        visited[start] = True
        HamiltonianGraph.is_hamiltonian(matrix, path, visited, n)
        return (True, path) if len(path)==n else (False, None)
            
# examples
# test_yes = np.array([[0, 1, 1, 1, 1], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1], [1, 0, 1, 0, 0], [1, 1, 1, 0, 0]])
# test_no = np.array([[0, 1, 0, 0], [1, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 0]])

# print(HamiltonianGraph.hamiltonian(test_yes))
# print(HamiltonianGraph.hamiltonian(test_no))