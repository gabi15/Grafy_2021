import math
from typing import Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import GraphConverter
from GraphReader import GraphReader
from GraphRepresentation import GraphRepresentation


class Digraph:
    def __init__(self):
        self.reader = GraphReader()
        # self.adjacency_matrix = None
        self.adjacency_matrix = np.array([[0, 1, 1, 0, 1, 0, 0],
                                          [1, 0, 1, 1, 1, 0, 1],
                                          [0, 0, 0, 0, 0, 1, 0],
                                          [0, 1, 0, 0, 0, 0, 1],
                                          [0, 0, 0, 0, 0, 0, 1],
                                          [0, 1, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 1, 0]], dtype=int)
        # self.vertices = -1
        self.vertices = 7

    def read_data(self, representation, filename) -> bool:
        """Read a graph from a file using given representation"""
        self.adjacency_matrix = self.reader.read_data(representation, filename)
        if self.adjacency_matrix is None:
            return False
        return True

    def get_digraph(self, output_representation) -> Union[np.ndarray, list, None]:
        """Return a graph in the given output representation"""
        return GraphConverter.convert_graph(self.adjacency_matrix, GraphRepresentation.ADJACENCY_MATRIX,
                                            output_representation)

    def save_to_file(self, representation, filename) -> bool:
        """Save a graph with given representation to the file with given name"""
        filename = "data/" + filename
        output_matrix = self.get_digraph(representation)
        if isinstance(output_matrix, list):
            with open(filename, "w+") as f:
                for row in output_matrix:
                    f.write(" ".join(str(item) for item in row))
                    f.write("\n")
            return True
        elif isinstance(output_matrix, np.ndarray):
            with open(filename, "w+") as f:
                np.savetxt(f, output_matrix, fmt="%i")
            return True
        else:
            return False

    def visualise_digraph(self, weight=False, save_to_file=False, file_name="") -> None:
        """Visualize directed graph"""
        G = nx.from_numpy_matrix(np.matrix(self.adjacency_matrix), create_using=nx.DiGraph)
        layout = nx.spiral_layout(G)
        nx.draw(G, layout, with_labels=True)

        if weight:
            labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)

        if save_to_file:
            plt.rcParams['savefig.format'] = 'png'
            plt.savefig("data/" + file_name)
        else:
            plt.show()

    def random_digraph(self, vertices, probability, weight=True, a=-5, b=10) -> None:
        if vertices < 2:
            raise Exception("Bad number of vertices")
        if probability > 1 or probability < 0:
            raise Exception("Bad probability")

        self.adjacency_matrix = np.zeros((vertices, vertices), dtype=int)
        for i in range(vertices):
            for j in range(vertices):
                if i != j:
                    r = random.random()
                    if r < probability and self.adjacency_matrix[j][i] == 0:
                        self.adjacency_matrix[i][j] = random.randint(a, b) if weight else 1

    def set_digraph(self, data) -> None:
        """Sets the adjacency matrix"""
        graph, representation = data
        self.adjacency_matrix = GraphConverter.convert_graph(graph, representation,
                                                             GraphRepresentation.ADJACENCY_MATRIX)
        self.vertices = self.adjacency_matrix.shape[0]

    def __str__(self) -> str:
        """Returns the adjacency matrix"""
        return '\n'.join([' '.join([str(u) for u in row]) for row in self.adjacency_matrix])

