import math
import networkx as netx
import matplotlib.pyplot as plt


def visualise_graph_on_circle(adjacency_matrix, save_to_file = False):
    nodes_number = len(adjacency_matrix)
    phi = 2 * math.pi / nodes_number
    graph_radius = 8
    plt.figure(figsize=(6, 6))

    nodes_positions = {}

    for node in range(nodes_number):
        nodes_positions.update({node: (math.cos(phi * node) * graph_radius, math.sin(phi * node) * graph_radius)})

    circular_graph = netx.from_numpy_matrix(adjacency_matrix)
    netx.draw_networkx(circular_graph, nodes_positions)
    plt.axis("off")

    if save_to_file:
        plt.savefig('circular_plot.png')
    else:
        plt.show()


''' przykladowa macierz sasiedztwa
arr = np.matrix([[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                 [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
                 [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                 [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
                 [0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]])
visualise_graph_on_circle(arr)
'''
