from typing import Union

import numpy as np

from GraphRepresentation import GraphRepresentation


def convert_graph(graph, input_representation, output_representation) -> Union[np.ndarray, list, None]:
    """Convert a graph from and to the given representations"""
    if input_representation == GraphRepresentation.ADJACENCY_MATRIX:
        return convert_from_adjacency_matrix(graph, output_representation)
    elif input_representation == GraphRepresentation.ADJACENCY_LIST:
        return convert_from_adjacency_list(graph, output_representation)
    elif input_representation == GraphRepresentation.INCIDENCE_MATRIX:
        return convert_from_incidence_matrix(graph, output_representation)


def convert_from_adjacency_matrix(graph, output_representation) -> Union[np.ndarray, list, None]:
    """Convert an adjacency matrix to the given representation"""
    if output_representation == GraphRepresentation.ADJACENCY_MATRIX:
        return graph
    elif output_representation == GraphRepresentation.ADJACENCY_LIST:
        return convert_adj_mat_to_adj_list(graph)
    elif output_representation == GraphRepresentation.INCIDENCE_MATRIX:
        return convert_adj_mat_to_inc_mat(graph)


def convert_from_adjacency_list(adjacency_list, output_representation) -> Union[np.ndarray, list, None]:
    """Convert an adjacency list to the given representation"""
    if output_representation == GraphRepresentation.ADJACENCY_MATRIX:
        return convert_adj_list_to_adj_mat(adjacency_list)
    elif output_representation == GraphRepresentation.ADJACENCY_LIST:
        return adjacency_list
    elif output_representation == GraphRepresentation.INCIDENCE_MATRIX:
        return convert_adj_list_to_inc_mat(adjacency_list)


def convert_from_incidence_matrix(graph, output_representation) -> Union[np.ndarray, list, None]:
    """Convert an incidence matrix to the given representation"""
    if output_representation == GraphRepresentation.ADJACENCY_MATRIX:
        return convert_inc_mat_to_adj_mat(graph)
    elif output_representation == GraphRepresentation.ADJACENCY_LIST:
        return convert_inc_mat_to_adj_list(graph)
    elif output_representation == GraphRepresentation.INCIDENCE_MATRIX:
        return graph


def convert_adj_list_to_adj_mat(adjacency_list) -> Union[np.ndarray, None]:
    """Convert an adjacency list to an adjacency matrix"""
    matrix_size = len(adjacency_list)
    matrix = np.zeros((matrix_size, matrix_size), dtype=int)
    try:
        for i, row in enumerate(adjacency_list):
            for item in row:
                matrix[i][item - 1] = 1
        return matrix
    except:
        return None


def convert_inc_mat_to_adj_mat(incidence_matrix) -> Union[np.ndarray, None]:
    """Convert an incidence matrix to an adjacency matrix"""
    matrix_size = len(incidence_matrix)
    matrix = np.zeros((matrix_size, matrix_size), dtype=int)
    for column in incidence_matrix.transpose():
        edge = []
        for i, item in enumerate(column):
            if item == 1:
                edge.append(i)
        if len(edge) != 2:
            return None
        matrix[edge[0]][edge[1]] = 1
        matrix[edge[1]][edge[0]] = 1
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


def convert_adj_list_to_inc_mat(adjacency_list) -> Union[np.ndarray, None]:
    """Convert an adjacency list to an incidence matrix"""
    try:
        adjacency_list = convert_adj_list_to_adj_mat(adjacency_list)
    except:
        return None
    return convert_adj_mat_to_inc_mat(adjacency_list)


def convert_inc_mat_to_adj_list(graph) -> Union[list, None]:
    """Convert an incidence matrix to an adjacency list"""
    try:
        graph = convert_inc_mat_to_adj_mat(graph)
    except:
        return None
    return convert_adj_mat_to_adj_list(graph)
