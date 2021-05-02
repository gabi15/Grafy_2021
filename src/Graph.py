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
        nx.draw(G, layout, with_labels=True)
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
        plt.show()

    def initialize_dijkstra_distances_positions(self, s) -> (list, list):
        """Initialize distances and positions arrays to perform Dijkstra's algorithm
        :param s: node to start with
        """
        ds = []
        ps = []
        for _ in self.adjacency_matrix:
            ds.append(sys.maxsize)
            ps.append(-1)

        ds[s] = 0
        return ds, ps

    def dijkstra(self, s) -> (list, list):
        """ Perform Dijkstra's algorithm starting with given node s
        :param s: given node to start with
        """
        (ds, ps) = self.initialize_dijkstra_distances_positions(s)
        S = []
        while len(S) != len(self.adjacency_matrix):
            temp_dist = [e if i not in S else sys.maxsize for i, e in enumerate(ds)]
            u = temp_dist.index(min(temp_dist))
            S.append(u)

            neighbours = []
            for i, val in enumerate(self.adjacency_matrix[u]):
                if val != 0:
                    neighbours.append(i)

            for idx in neighbours:
                v = idx
                new_dist = self.adjacency_matrix[u][v] + ds[u]

                if ds[v] > new_dist:
                    ds[v] = new_dist
                    ps[v] = u

        return ds, ps

    def print_dijkstra(self, s=0) -> bool:
        """ Print result of Dijkstra's algorithm to standard output
        :param s: given node to start with
        """
        (ds, ps) = self.dijkstra(s)
        result = f'START: s = {s}:'

        for index in range(len(self.adjacency_matrix)):
            if ds[index] == sys.maxsize:
                return False

            result += f'\nd({index})={ds[index]}\t\t==> ['
            trail = [index]

            while ps[index] > 0:
                trail.append(ps[index])
                index = ps[index]

            result += ' - '.join(map(lambda v: str(v), reversed(trail)))
            result += ']'
        print(result)
        return True

    def find_distance_matrix(self) -> np.ndarray:
        """Find the distance between every two nodes"""
        n = len(self.adjacency_matrix)
        distance_matrix = np.zeros((n, n))

        for i in range(n):
            ds, ps = self.dijkstra(s=i)
            distance_matrix[i] = ds

        return distance_matrix

    def set_graph(self, data) -> None:
        """Sets the adjacency matrix"""
        graph, representation = data
        self.adjacency_matrix = GraphConverter.convert_graph(graph, representation,
                                                             GraphRepresentation.ADJACENCY_MATRIX)

    def __str__(self) -> str:
        """Returns the adjacency matrix"""
        return '\n'.join([' '.join([str(u) for u in row]) for row in self.adjacency_matrix])
