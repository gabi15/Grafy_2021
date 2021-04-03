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
    def random_graph_edges(n, m):
        try:
            if n < 2:
                raise BadNumberOfVertices
            if m > n * (n - 1) / 2 or m <= 0:
                raise BadNumberOfEdges
        except BadNumberOfVertices:
            print("number of edges and vertices must be bigger than 1")
            return None
        except BadNumberOfEdges:
            print("enter correct number of edges please")
            return None
        matrix = np.zeros((n, m), dtype=int)
        i = 0
        while i < m:
            first_rand = random.randint(0, n - 1)
            second_rand = random.randint(0, n - 1)
            while first_rand == second_rand:
                second_rand = random.randint(0, n - 1)
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
    def random_graph_probability(n, p):  # creates a graph using the incidence matrix
        try:
            if n < 2:
                raise BadNumberOfVertices
            if p > 1 or p < 0:
                raise BadProbability
        except BadNumberOfVertices:
            print("number of vertices must be bigger than 1")
            return None
        except BadProbability:
            print("probability must be between 0 and 1")
            return None
        matrix = np.zeros((n, n), dtype=int)

        for i in range(n):
            for j in range(i + 1, n):
                r = random.random()
                if r < p:
                    matrix[i][j] = matrix[j][i] = 1
        return matrix


    # example
    # input_n = 5
    # input_p = 0.4
    # random_probability_to_file(input_n,input_p, 'result.txt')