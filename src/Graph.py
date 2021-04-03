from GraphReader import GraphReader
from GraphConverter import GraphConverter
from RandomGraphGenerator import RandomGraphGenerator
from GraphRepresentation import GraphRepresentation
import math
import matplotlib.pyplot as plt
import numpy as np
import networkx as netx


class Graph:
    graph_reader = GraphReader()
    graph_converter = GraphConverter()
    graph_generator = RandomGraphGenerator()
    adjacency_matrix = None

    def read_data(self, representation, filename):
        self.adjacency_matrix = self.graph_reader.read_data(representation, filename)
        if self.adjacency_matrix is None:
            return False
        return True

    def get_graph(self, output_representation):
        return self.graph_converter.convert_graph(self.adjacency_matrix,GraphRepresentation.ADJACENCY_MATRIX, output_representation)

    def save_to_file(self, representation, filename):
        filename = "../data/" + filename
        output_matrix = self.get_graph(representation)
        if isinstance(output_matrix, list):
            with open(filename, "w") as f:
                for row in output_matrix:
                    f.write(" ".join(str(item) for item in row))
                    f.write("\n")
            return True
        elif isinstance(output_matrix, np.ndarray):
            np.savetxt(filename, output_matrix, fmt="%i")
            return True
        else:
            return False

    def visualise_graph_on_circle(self, save_to_file=False):
        nodes_number = len(self.adjacency_matrix)
        phi = 2 * math.pi / nodes_number
        graph_radius = 8
        plt.figure(figsize=(6, 6))

        nodes_positions = {}

        for node in range(nodes_number):
            nodes_positions.update({node: (math.cos(phi * node) * graph_radius, math.sin(phi * node) * graph_radius)})

        circular_graph = netx.from_numpy_matrix(self.adjacency_matrix)
        netx.draw_networkx(circular_graph, nodes_positions)
        plt.axis("off")

        if save_to_file:
            plt.savefig('../data/circular_plot.png')
        else:
            plt.show()

    def print_graph_matrix(self):
        print(self.adjacency_matrix)

    def generate_NL_graph(self, n, l):
        self.adjacency_matrix = self.graph_generator.random_graph_edges(n, l)
        if self.adjacency_matrix is None:
            return False
        return True

    def generate_NP_graph(self, n, p):
        graph = self.graph_generator.random_graph_probability(n, p)
        if graph is not None:
            self.adjacency_matrix = self.graph_converter.convert_graph(graph, GraphRepresentation.INCIDENCE_MATRIX, GraphRepresentation.ADJACENCY_MATRIX)
        if self.adjacency_matrix is None:
            return False
        return True
