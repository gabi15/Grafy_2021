from typing import Union

import numpy as np

from GraphRepresentation import GraphRepresentation


class IncorrectInputException(Exception):
    """Exception raised in case of bad input"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Incorrect input - " + self.message


def is_square(matrix) -> bool:
    """Check if a matrix is square"""
    if matrix.ndim == 0:
        return True
    elif matrix.ndim == 2:
        return matrix.shape[0] == matrix.shape[1]
    return False


def is_symmetrical(matrix) -> bool:
    """Check if the matrix is symmetrical"""
    transpose_matrix = matrix.transpose()
    comparision = transpose_matrix == matrix
    return comparision.all()


def has_zeros_on_diagonal(matrix) -> bool:
    """Check if the matrix has zeros on diagonal"""
    if matrix.ndim == 0:
        if matrix == 0:
            return True
        return False
    elif matrix.ndim == 2:
        for i, row in enumerate(matrix):
            if row[i] != 0:
                return False
        return True
    return False


def convert_graph(graph, input_representation, output_representation) -> Union[np.ndarray, list]:
    """Convert a graph from and to the given representations"""
    if input_representation == GraphRepresentation.ADJACENCY_MATRIX:
        return convert_from_adjacency_matrix(graph, output_representation)
    elif input_representation == GraphRepresentation.ADJACENCY_LIST:
        return convert_from_adjacency_list(graph, output_representation)
    elif input_representation == GraphRepresentation.INCIDENCE_MATRIX:
        return convert_from_incidence_matrix(graph, output_representation)
    elif input_representation == GraphRepresentation.GRAPHICAL_SEQUENCE:
        return convert_from_graphical_sequence(graph, output_representation)


def convert_from_adjacency_matrix(graph, output_representation) -> Union[np.ndarray, list]:
    """Convert an adjacency matrix to the given representation"""
    if output_representation == GraphRepresentation.ADJACENCY_MATRIX:
        return graph
    elif output_representation == GraphRepresentation.ADJACENCY_LIST:
        return convert_adj_mat_to_adj_list(graph)
    elif output_representation == GraphRepresentation.INCIDENCE_MATRIX:
        return convert_adj_mat_to_inc_mat(graph)


def convert_from_adjacency_list(adjacency_list, output_representation) -> Union[np.ndarray, list]:
    """Convert an adjacency list to the given representation"""
    if output_representation == GraphRepresentation.ADJACENCY_MATRIX:
        return convert_adj_list_to_adj_mat(adjacency_list)
    elif output_representation == GraphRepresentation.ADJACENCY_LIST:
        return adjacency_list
    elif output_representation == GraphRepresentation.INCIDENCE_MATRIX:
        return convert_adj_list_to_inc_mat(adjacency_list)


def convert_from_incidence_matrix(graph, output_representation) -> Union[np.ndarray, list]:
    """Convert an incidence matrix to the given representation"""
    if output_representation == GraphRepresentation.ADJACENCY_MATRIX:
        return convert_inc_mat_to_adj_mat(graph)
    elif output_representation == GraphRepresentation.ADJACENCY_LIST:
        return convert_inc_mat_to_adj_list(graph)
    elif output_representation == GraphRepresentation.INCIDENCE_MATRIX:
        return graph


def convert_from_graphical_sequence(graphical_sequence, output_representation):
    if output_representation == GraphRepresentation.ADJACENCY_LIST:
        return convert_edge_list_to_adj_list(convert_graph_seq_to_edge_list(graphical_sequence), len(graphical_sequence))


def convert_adj_list_to_adj_mat(adjacency_list) -> np.ndarray:
    """Convert an adjacency list to an adjacency matrix"""
    matrix_size = len(adjacency_list)
    matrix = np.zeros((matrix_size, matrix_size), dtype=int)
    try:
        for i, row in enumerate(adjacency_list):
            for item in row:
                matrix[i][item - 1] = 1

    except Exception:
        raise IncorrectInputException("Index of list is out of matrix bounds")
    if not is_symmetrical(matrix):
        raise IncorrectInputException("Matrix built from adjacency list is not symmetrical")
    if not has_zeros_on_diagonal(matrix):
        raise IncorrectInputException("Matrix built from adjacency list has non zero value on diagonal")
    return matrix


def convert_inc_mat_to_adj_mat(incidence_matrix) -> np.ndarray:
    """Convert an incidence matrix to an adjacency matrix"""
    matrix_size = len(incidence_matrix)
    matrix = np.zeros((matrix_size, matrix_size), dtype=int)
    for column in incidence_matrix.transpose():
        edge = []
        for i, item in enumerate(column):
            if item == 1:
                edge.append(i)
        if len(edge) != 2:
            raise IncorrectInputException("The edge should connect two different vertices")
        matrix[edge[0]][edge[1]] = 1
        matrix[edge[1]][edge[0]] = 1
    if not is_symmetrical(matrix):
        raise IncorrectInputException("Matrix built from incidence matrix is not symmetrical")
    if not has_zeros_on_diagonal(matrix):
        raise IncorrectInputException("Matrix built from incidence matrix has non zero value on diagonal")
    return matrix


def convert_adj_mat_to_adj_list(graph) -> list:
    """Convert an adjacency matrix to an adjacency list"""
    adjacency_list = []
    for row in graph:
        neighbors = []
        for i, item in enumerate(row):
            if item == 1:
                neighbors.append(i + 1)
        adjacency_list.append(neighbors)
    return adjacency_list


def convert_adj_mat_to_inc_mat(graph) -> np.ndarray:
    """Convert an adjacency matrix to an incidence matrix"""
    incidence_matrix = []
    row_length = graph[0].size
    for i, row in enumerate(graph):
        for j in range(i):
            if row[j] == 1:
                edge = np.zeros(row_length, dtype=int)
                edge[i] = 1
                edge[j] = 1
                incidence_matrix.append(edge)
    incidence_matrix = np.array(incidence_matrix).transpose()
    return incidence_matrix


def convert_adj_list_to_inc_mat(adjacency_list) -> np.ndarray:
    """Convert an adjacency list to an incidence matrix"""

    adjacency_list = convert_adj_list_to_adj_mat(adjacency_list)

    return convert_adj_mat_to_inc_mat(adjacency_list)


def convert_inc_mat_to_adj_list(graph) -> list:
    """Convert an incidence matrix to an adjacency list"""

    graph = convert_inc_mat_to_adj_mat(graph)

    return convert_adj_mat_to_adj_list(graph)


def convert_graph_seq_to_edge_list(graphical_sequence):
    graphical_sequence = sorted(graphical_sequence, reverse=True)
    nodes = [[node_index, node_grade, 0] for node_index, node_grade in enumerate(graphical_sequence)]
    adjacency_set = set()

    for i in range(int(sum(graphical_sequence) / 2)):
        nodes = [node for node in nodes if node[1] > node[2]]

        for nodes_left in sorted(nodes[1:], key=lambda x: (x[1] - x[2], x[1]), reverse=True):
            edge = {nodes[0][0]+1, nodes_left[0]+1}

            if edge not in adjacency_set:
                adjacency_set.add(frozenset(edge))
                nodes[0][2] += 1
                nodes_left[2] += 1
                break

    adjacency_list = [list(row) for row in adjacency_set]
    adjacency_list.sort(key=lambda x: (x[0], x[1]))
    return adjacency_list


def convert_edge_list_to_adj_list(edge_list,n):
    edges = [[] for _ in range(n)]
    for i in edge_list:
        edges[i[0] - 1].append(i[1])
        edges[i[1] - 1].append(i[0])
    return edges
