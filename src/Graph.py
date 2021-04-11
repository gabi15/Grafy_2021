from GraphReader import GraphReader
from GraphConverter import GraphConverter
from RandomGraphGenerator import RandomGraphGenerator
from GraphRepresentation import GraphRepresentation
from copy import deepcopy
import math
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import random


class Graph:
    reader = GraphReader()
    converter = GraphConverter()
    generator = RandomGraphGenerator()
    adjacency_matrix = None

    def read_data(self, representation, filename):
        self.adjacency_matrix = self.reader.read_data(representation, filename)
        if self.adjacency_matrix is None:
            return False
        return True

    def get_graph(self, output_representation):
        return self.converter.convert_graph(self.adjacency_matrix, GraphRepresentation.ADJACENCY_MATRIX,
                                            output_representation)

    def save_to_file(self, representation, filename):
        filename = "data/" + filename
        output_matrix = self.get_graph(representation)
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

    def visualise_graph_on_circle(self, save_to_file=False):
        nodes_number = len(self.adjacency_matrix)
        phi = 2 * math.pi / nodes_number
        graph_radius = 8
        plt.figure(figsize=(6, 6))

        nodes_positions = {}

        for node in range(nodes_number):
            nodes_positions.update({node: (math.cos(phi * node) * graph_radius, math.sin(phi * node) * graph_radius)})

        circular_graph = nx.from_numpy_matrix(self.adjacency_matrix)
        nx.draw_networkx(circular_graph, nodes_positions)
        plt.axis("off")

        if save_to_file:
            plt.savefig('data/circular_plot.png')
        else:
            plt.show()

    def print_graph_matrix(self):
        print(self.adjacency_matrix)

    def generate_NL_graph(self, n, l):
        graph = self.generator.random_graph_edges(n, l)
        if graph is not None:
            self.adjacency_matrix = self.converter.convert_graph(graph, GraphRepresentation.INCIDENCE_MATRIX,
                                                                 GraphRepresentation.ADJACENCY_MATRIX)
        if self.adjacency_matrix is None:
            return False
        return True

    def generate_NP_graph(self, n, p):
        graph = self.generator.random_graph_probability(n, p)
        if graph is not None:
            self.adjacency_matrix = graph
            return True
        return False

    def randomize_graph_edges(self):
        adjacency_list = self.converter.convert_adj_mat_to_adj_list(self.adjacency_matrix)
        adjacency_list_copy = deepcopy(adjacency_list)
        flattened_list = [item for sublist in adjacency_list for item in sublist]

        if len(adjacency_list) == 2:
            return False

        while True:
            first, second = random.choices(flattened_list, k=2)
            old_first, old_second = random.choices(flattened_list, k=2)

            # TODO skrocic, rozdzielic, uproscic
            if not(first == second) \
                    and (first not in adjacency_list[second-1])\
                    and not (old_first == old_second) \
                    and (old_first in adjacency_list[old_second - 1]) \
                    and not (old_first == first and old_second == second)\
                    and not (old_second == first and old_first == second):

                adjacency_list_copy[old_second-1].remove(old_first)
                adjacency_list_copy[old_first-1].remove(old_second)

                adjacency_list_copy[first-1].append(second)
                adjacency_list_copy[second-1].append(first)
                break

        self.adjacency_matrix = self.converter.convert_adj_list_to_adj_mat(adjacency_list_copy)
        return True
