import numpy as np
import random
import RandomGraphGenerator as rgg
import GraphConverter as gc
import GraphRepresentation as gr


def draw_random_weights(adj_mat) -> np.ndarray:
    for i in range(len(adj_mat)):
        for j in range(len(adj_mat)):
            if adj_mat[i][j] == 1:
                adj_mat[i][j] = random.randint(1, 10)
    return adj_mat


def random_weighted_graph_edges(vertices: int, edges: int) -> (np.ndarray, gr.GraphRepresentation):
    """Generate random weighted adjacency matrix for given number of vertices and edges"""
    inc_mat = rgg.random_graph_edges(vertices, edges)
    adj_mat = gc.convert_graph(inc_mat, gr.GraphRepresentation.INCIDENCE_MATRIX, gr.GraphRepresentation.ADJACENCY_MATRIX)

    draw_random_weights(adj_mat)

    return adj_mat


def random_weighted_graph_probability(vertices: int, probability: float) -> (np.ndarray, gr.GraphRepresentation):
    """Generate random weighted adjacency matrix for given number of vertices and probability"""
    adj_mat = rgg.random_graph_probability(vertices, probability)

    draw_random_weights(adj_mat)

    return adj_mat
