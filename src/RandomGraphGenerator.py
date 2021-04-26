import numpy as np
import random


class BadNumberOfEdges(Exception):
    """Raised when number of Edges is too big """


class BadNumberOfVertices(Exception):
    """Raised when number of vertices is smaller than 2 """


class BadProbability(Exception):
    """Raised when value of probability is less than 0 or more than 1 """


class RandomGraphGenerator:

    @staticmethod
    def random_graph_edges(vertices: int, edges: int) -> np.ndarray:
        """Generate random incidence matrix for given number of vertices and edges"""
        if vertices < 2:
            raise BadNumberOfVertices
        if edges > vertices * (vertices - 1) / 2 or edges <= 0:
            raise BadNumberOfEdges
        matrix = np.zeros((vertices, edges), dtype=int)
        i = 0
        while i < edges:
            first_rand = random.randint(0, vertices - 1)
            second_rand = random.randint(0, vertices - 1)
            while first_rand == second_rand:
                second_rand = random.randint(0, vertices - 1)
            is_duplicated = False
            for j in range(i):
                if matrix[first_rand][j] == 1 and matrix[second_rand][j] == 1:
                    is_duplicated = True
                    break

            if not is_duplicated:
                matrix[first_rand][i] = 1
                matrix[second_rand][i] = 1
                i += 1
        return matrix

    @staticmethod
    def random_graph_probability(n, p):
        """Generate random adjacency matrix for given number of vertices and probability"""
        if n < 2:
            raise BadNumberOfVertices
        if p > 1 or p < 0:
            raise BadProbability
        matrix = np.zeros((n, n), dtype=int)

        for i in range(n):
            for j in range(i + 1, n):
                r = random.random()
                if r < p:
                    matrix[i][j] = matrix[j][i] = 1
        return matrix