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
        filename = "./../data/" + filename
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
        # estimate graph radius
        graph_radius = nodes_number * 1.27 + 1.69

        nodes = []

        for node in range(nodes_number):
            nodes.insert(node, (math.cos(phi * node) * graph_radius, math.sin(phi * node) * graph_radius))

        figure, axes = plt.subplots()
        axes.set_aspect(1)

        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix[0])):
                if self.adjacency_matrix[i][j] == 1:
                    (x, y) = nodes[i]
                    (x2, y2) = nodes[j]
                    plt.plot([x/20+0.5, x2/20+0.5], [y/20+0.5, y2/20+0.5], 'r-', linewidth=2, zorder=1)

        i = 0
        for node in nodes:
            (x, y) = node
            i += 1
            circle_border = plt.Circle((x/20+0.5, y/20+0.5), radius=0.07*nodes_number/10, color='black', zorder=2)
            circle = plt.Circle((x/20+0.5, y/20+0.5), radius=0.06*nodes_number/10, color='green', zorder=3)
            axes.add_patch(circle_border)
            axes.add_patch(circle)
            if nodes_number <= 20:
                font_size = 16
            else:
                font_size = 20
            axes.annotate(i, xy=(x/20+0.5, y/20+0.5), fontsize=font_size, color='white', verticalalignment='center', horizontalalignment='center')

        plt.axis("off")
        axes.set_aspect('equal')

        if save_to_file:
            plt.savefig('data/circular_plot.png')
        else:
            plt.show()

    def visualise_graph(self, save_to_file=False):
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

    def randomize_graph_edges(self, number_of_randomizations):
        adjacency_list = self.converter.convert_adj_mat_to_adj_list(self.adjacency_matrix)
        adjacency_list_copy = deepcopy(adjacency_list)
        flattened_list = [item for sublist in adjacency_list for item in sublist]

        # 3 or less vertices - to few to randomize
        if len(adjacency_list) <= 3:
            return False

        # estimate number or randomizations that is possible to perform
        free_edges_counter = 0
        n = len(adjacency_list)
        for i in adjacency_list:
            free_edges_counter += n - 1 - len(i)
        free_edges_counter /= 2

        # estimate number of failed attempts to perform a single randomization
        fail = 0
        while fail < 15:
            # get random (reasonable) number of randomizations
            if number_of_randomizations == 0:
                edges_to_randomize = random.randint(1, free_edges_counter)
            else:
                # number of randomizations to perform cannot be greater than estimated maximal number of randomizations
                if number_of_randomizations > free_edges_counter:
                    return False
                else:
                    edges_to_randomize = number_of_randomizations

            # check if we didn't fall into an endless loop
            endless_loop_flag = 0

            # if we still should perform randomizing or didn't fall into endless loop
            while edges_to_randomize > 0 and endless_loop_flag <= 20:
                first_start, first_end, second_start, second_end = random.sample(set(flattened_list), k=4)

                # random nodes aren't connected in a way that would prevent randomizing (when one node is connected to two other)
                if (first_start in adjacency_list_copy[first_end - 1]) and (second_start in adjacency_list_copy[second_end - 1]):
                    if (first_start not in adjacency_list_copy[second_end - 1]) and (second_start not in adjacency_list_copy[first_end - 1]):
                        # remove existing connections
                        adjacency_list_copy[first_start-1].remove(first_end)
                        adjacency_list_copy[first_end-1].remove(first_start)
                        adjacency_list_copy[second_start-1].remove(second_end)
                        adjacency_list_copy[second_end-1].remove(second_start)

                        # add new connections
                        adjacency_list_copy[first_start - 1].append(second_end)
                        adjacency_list_copy[second_end - 1].append(first_start)
                        adjacency_list_copy[second_start - 1].append(first_end)
                        adjacency_list_copy[first_end - 1].append(second_start)
                        edges_to_randomize -= 1

                    # other randomization is possible
                    elif (first_start not in adjacency_list_copy[second_start - 1]) and (second_end not in adjacency_list_copy[first_end - 1]):
                        adjacency_list_copy[first_start - 1].remove(first_end)
                        adjacency_list_copy[first_end - 1].remove(first_start)
                        adjacency_list_copy[second_start - 1].remove(second_end)
                        adjacency_list_copy[second_end - 1].remove(second_start)

                        adjacency_list_copy[first_start - 1].append(second_start)
                        adjacency_list_copy[second_start - 1].append(first_start)
                        adjacency_list_copy[second_end - 1].append(first_end)
                        adjacency_list_copy[first_end - 1].append(second_end)
                        edges_to_randomize -= 1
                endless_loop_flag += 1

            if endless_loop_flag > 20:
                fail += 1
            elif edges_to_randomize == 0:
                self.adjacency_matrix = self.converter.convert_adj_list_to_adj_mat(adjacency_list_copy)
                return True
        return False
