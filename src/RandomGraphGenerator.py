import numpy as np
import random

from GraphRepresentation import GraphRepresentation
from GraphConverter import convert_adj_list_to_adj_mat, convert_edge_list_to_adj_list, convert_graph_seq_to_edge_list
from Graph import Graph


class BadNumberOfEdges(Exception):
    """Raised when number of edges is too big """

    def __str__(self):
        return "The number of edges is too big"


class BadNumberOfVertices(Exception):
    """Raised when number of vertices is smaller than 2 """

    def __str__(self):
        return "The number of vertices is smaller than 2"


class BadProbability(Exception):
    """Raised when value of probability is less than 0 or more than 1 """

    def __str__(self):
        return "The value of probability is less than 0 or more than 1"


class BadDegree(Exception):
    """Raised when degree is less than 1 or bigger than the number of vertices """

    def __str__(self):
        return "The degree is less than 1 or more than the number of vertices"


class BadNKValues(Exception):
    """Raised when there is no graph with given degree and number of vertices """

    def __str__(self):
        return "There is no graph with given degree and number of vertices (vertices * degree is uneven)"


def random_graph_edges(vertices: int, edges: int) -> (np.ndarray, GraphRepresentation):
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
    return matrix, GraphRepresentation.INCIDENCE_MATRIX


def random_graph_probability(vertices: int, probability: float) -> (np.ndarray, GraphRepresentation):
    """Generate random adjacency matrix for given number of vertices and probability"""
    if vertices < 2:
        raise BadNumberOfVertices
    if probability > 1 or probability < 0:
        raise BadProbability
    matrix = np.zeros((vertices, vertices), dtype=int)
    for i in range(vertices):
        for j in range(i + 1, vertices):
            r = random.random()
            if r < probability:
                matrix[i][j] = matrix[j][i] = 1
    return matrix, GraphRepresentation.ADJACENCY_MATRIX


def random_graph_regular(vertices: int, degree: int) -> (np.ndarray, GraphRepresentation):
    """Generate random adjacency matrix for given degree and number of vertices"""
    if vertices < 2:
        raise BadNumberOfVertices
    if degree < 1 or degree >= vertices:
        raise BadDegree
    if (vertices * degree) % 2 != 0:
        raise BadNKValues

    graph_seq = [degree for i in range(vertices)]
    matrix = convert_adj_list_to_adj_mat(
        convert_edge_list_to_adj_list(convert_graph_seq_to_edge_list(graph_seq), vertices))

    g = Graph()
    g.set_graph((matrix, GraphRepresentation.ADJACENCY_MATRIX))
    g.randomize_graph_edges(100)

    return g.adjacency_matrix, GraphRepresentation.ADJACENCY_MATRIX
