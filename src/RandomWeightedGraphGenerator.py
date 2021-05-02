import numpy as np
import random
import RandomGraphGenerator as rgg
import GraphConverter as gc
import GraphRepresentation as gr


def draw_random_weights(adj_mat):
    adj_mat_size = len(adj_mat)
    for i in range(adj_mat_size):
        for j in range(adj_mat_size):
            if adj_mat[i][j] == 1:
                adj_mat[i][j] = random.randint(1, 10)
    return adj_mat


def random_weighted_graph_edges(vertices: int, edges: int) -> (np.ndarray, gr.GraphRepresentation):
    """Generate random weighted adjacency matrix for given number of vertices and edges"""
    inc_mat, rep = rgg.random_graph_edges(vertices, edges)
    adj_mat = gc.convert_graph(inc_mat, rep, gr.GraphRepresentation.ADJACENCY_MATRIX)
    draw_random_weights(adj_mat)
    return adj_mat


def random_weighted_graph_probability(vertices: int, probability: float) -> (np.ndarray, gr.GraphRepresentation):
    """Generate random weighted adjacency matrix for given number of vertices and probability"""
    adj_mat, rep = rgg.random_graph_probability(vertices, probability)
    draw_random_weights(adj_mat)
    return adj_mat
