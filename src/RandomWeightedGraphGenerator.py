import numpy as np
import random
import RandomGraphGenerator as rgg
import GraphRepresentation as gr


def draw_random_weights(adj_mat):
    """Generate random weights using given adjacency matrix
    :param adj_mat: given adjacency matrix of a non-weighted graph
    :return: adjacency matrix with weighted vertices
    """
    adj_mat_size = len(adj_mat)
    for i in range(adj_mat_size):
        for j in range(i):
            if i != j and adj_mat[i][j] == 1:
                random_weight = random.randint(1, 10)
                adj_mat[i][j] = random_weight
                adj_mat[j][i] = random_weight
    return adj_mat


def random_weighted_graph_edges(vertices: int, edges: int) -> (np.ndarray, gr.GraphRepresentation):
    """Generate random weighted adjacency matrix for given number of vertices and edges"""
    adj_mat, _ = rgg.random_graph_edges(vertices, edges)
    return draw_random_weights(adj_mat), gr.GraphRepresentation.ADJACENCY_MATRIX


def random_weighted_graph_probability(vertices: int, probability: float) -> (np.ndarray, gr.GraphRepresentation):
    """Generate random weighted adjacency matrix for given number of vertices and probability"""
    adj_mat, _ = rgg.random_graph_probability(vertices, probability)
    return draw_random_weights(adj_mat), gr.GraphRepresentation.ADJACENCY_MATRIX
