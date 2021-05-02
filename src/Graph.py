import math
import sys
from typing import Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import GraphConverter
from GraphReader import GraphReader
from GraphRepresentation import GraphRepresentation


class Graph:
    def __init__(self):
        self.reader = GraphReader()
        self.adjacency_matrix = None

    def read_data(self, representation, filename) -> bool:
        """Read a graph from a file using given representation"""
        self.adjacency_matrix = self.reader.read_data(representation, filename)
        if self.adjacency_matrix is None:
            return False
        return True

    def get_graph(self, output_representation) -> Union[np.ndarray, list, None]:
        """Return a graph in the given output representation"""
        return GraphConverter.convert_graph(self.adjacency_matrix, GraphRepresentation.ADJACENCY_MATRIX,
                                            output_representation)

    def save_to_file(self, representation, filename) -> bool:
        """Save a graph with given representation to the file with given name"""
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

    def visualise_graph_on_circle(self, save_to_file, file_name) -> None:
        """Visualize graph on a circle. Return visualization or save to file.
        :param save_to_file: if True, the graph will be saved to file_name file
        :param file_name file name for the graph"""
        nodes_number = len(self.adjacency_matrix)
        phi = 2 * math.pi / nodes_number
        # estimate graph radius
        graph_radius = nodes_number * 1.5

        nodes = []

        for node in range(nodes_number):
            nodes.insert(node, (math.cos(phi * node) * graph_radius, math.sin(phi * node) * graph_radius))

        plt.close()
        figure, axes = plt.subplots()
        axes.set_aspect(1)
        figure.set_size_inches(8, 8)

        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix[0])):
                if self.adjacency_matrix[i][j] == 1:
                    (x, y) = nodes[i]
                    (x2, y2) = nodes[j]
                    plt.plot([x / 15 + 0.5, x2 / 15 + 0.5], [y / 15 + 0.5, y2 / 15 + 0.5], 'r-', linewidth=2, zorder=1)

        i = 0
        for node in nodes:
            (x, y) = node
            i += 1
            circle_border = plt.Circle((x / 15 + 0.5, y / 15 + 0.5), radius=0.07 * nodes_number / 10, color='black',
                                       zorder=2)
            circle = plt.Circle((x / 15 + 0.5, y / 15 + 0.5), radius=0.06 * nodes_number / 10, color='green', zorder=3)
            axes.add_patch(circle_border)
            axes.add_patch(circle)
            if nodes_number <= 20:
                font_size = 16
            else:
                font_size = 20
            axes.annotate(i, xy=(x / 15 + 0.5, y / 15 + 0.5), fontsize=font_size, color='white',
                          verticalalignment='center', horizontalalignment='center')

        plt.axis("off")
        axes.set_aspect('equal')

        if save_to_file:
            plt.rcParams['savefig.format'] = 'png'
            plt.savefig("data/" + file_name)
        else:
            plt.show()

    def visualize_graph_with_weights(self) -> None:
        """Visualize weighted graph"""
        G = nx.from_numpy_matrix(np.matrix(self.adjacency_matrix), create_using=nx.DiGraph)
        layout = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw(G, layout, with_labels=True)
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
        plt.show()

    def initialize_dijkstra_distances_positions(self, starting_node) -> (list, list):
        """Initialize distances and positions arrays to perform Dijkstra's algorithm
        :param starting_node: node to start with
        """
        distances = []
        positions = []
        for _ in self.adjacency_matrix:
            distances.append(sys.maxsize)
            positions.append(-1)

        distances[starting_node] = 0
        return distances, positions

    def relax_dijkstra(self, distances, positions, u, u_neighbours):
        for v in u_neighbours:
            new_dist = self.adjacency_matrix[u][v] + distances[u]

            if distances[v] > new_dist:
                distances[v] = new_dist
                positions[v] = u

        return distances, positions

    def dijkstra(self, starting_node) -> (list, list):
        """ Perform Dijkstra's algorithm starting with given node s
        :param starting_node: given node to start with
        """
        (distances, positions) = self.initialize_dijkstra_distances_positions(starting_node)
        ready_nodes = []
        while len(ready_nodes) != len(self.adjacency_matrix):
            not_ready_nodes = [val if i not in ready_nodes else sys.maxsize for i, val in enumerate(distances)]
            u = not_ready_nodes.index(min(not_ready_nodes))
            ready_nodes.append(u)

            u_neighbours = []
            [u_neighbours.append(i) if val != 0 else None for i, val in enumerate(self.adjacency_matrix[u])]

            distances, positions = self.relax_dijkstra(distances, positions, u, u_neighbours)

        return distances, positions

    def print_dijkstra(self, starting_node=0) -> bool:
        """ Print result of Dijkstra's algorithm to standard output starting with either node 0 or given node
        :param starting_node: given node to start with
        """
        (distances, positions) = self.dijkstra(starting_node)
        result_paths = f'START: s = {starting_node}:'

        for index in range(len(self.adjacency_matrix)):
            if distances[index] == sys.maxsize:
                return False

            result_paths += f'\nd({index})={distances[index]}\t\t==> ['
            node = [index]

            while positions[index] > 0:
                node.append(positions[index])
                index = positions[index]

            result_paths += ' - '.join(map(lambda v: str(v), reversed(node)))
            result_paths += ']'
        print(result_paths)
        return True

    def find_distances_matrix(self) -> np.ndarray:
        """Find the distances between every two nodes"""
        adj_mat_size = len(self.adjacency_matrix)
        distances_matrix = np.zeros((adj_mat_size, adj_mat_size))

        for node in range(adj_mat_size):
            distances, _ = self.dijkstra(starting_node=node)
            distances_matrix[node] = distances

        return distances_matrix

    def set_graph(self, data) -> None:
        """Sets the adjacency matrix"""
        graph, representation = data
        self.adjacency_matrix = GraphConverter.convert_graph(graph, representation,
                                                             GraphRepresentation.ADJACENCY_MATRIX)

    def __str__(self) -> str:
        """Returns the adjacency matrix"""
        return '\n'.join([' '.join([str(u) for u in row]) for row in self.adjacency_matrix])
