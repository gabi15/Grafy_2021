import sys
from typing import Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import GraphConverter
from GraphReader import GraphReader
from GraphReader import IncorrectInputException
from GraphRepresentation import GraphRepresentation


class Digraph:
    def __init__(self):
        self.reader = GraphReader()
        # self.adjacency_matrix = None
        # self.adjacency_matrix = np.array([[0, 1, 1, 0, 1, 0, 0],
        #                                   [1, 0, 1, 1, 1, 0, 1],
        #                                   [0, 0, 0, 0, 0, 1, 0],
        #                                   [0, 1, 0, 0, 0, 0, 1],
        #                                   [0, 0, 0, 0, 0, 0, 1],
        #                                   [0, 1, 0, 0, 0, 0, 0],
        #                                   [0, 0, 0, 0, 0, 1, 0]], dtype=int)
        # self.edges_matrix = np.array([[0, 1, 1, 0, 1, 0, 0],
        #                               [1, 0, 1, 1, 1, 0, 1],
        #                               [0, 0, 0, 0, 0, 1, 0],
        #                               [0, 1, 0, 0, 0, 0, 1],
        #                               [0, 0, 0, 0, 0, 0, 1],
        #                               [0, 1, 0, 0, 0, 0, 0],
        #                               [0, 0, 0, 0, 0, 1, 0]], dtype=int)
        # self.vertices = 7
        self.adjacency_matrix = np.array([[0, 6, 3, 0, -1, 0, 0],
                                          [10, 0, -5, -4, 4, 0, 4],
                                          [0, 0, 0, 0, 0, 2, 0],
                                          [0, 5, 0, 0, 0, 0, 9],
                                          [0, 0, 0, 0, 0, 0, -4],
                                          [0, 9, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 4, 0]], dtype=int)
        self.edges_matrix = np.array([[0, 1, 1, 0, 1, 0, 0],
                                      [1, 0, 1, 1, 1, 0, 1],
                                      [0, 0, 0, 0, 0, 1, 0],
                                      [0, 1, 0, 0, 0, 0, 1],
                                      [0, 0, 0, 0, 0, 0, 1],
                                      [0, 1, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 1, 0]], dtype=int)
        self.vertices = 7
        # self.adjacency_matrix = np.array([[0, 3, 8, 0, -4],
        #                                   [0, 0, 0, 1, 7],
        #                                   [0, 4, 0, 0, 0],
        #                                   [2, 0, -5, 0, 0],
        #                                   [0, 0, 0, 6, 0]], dtype=int)
        # self.edges_matrix = np.array([[0, 1, 1, 0, 1],
        #                               [0, 0, 0, 1, 1],
        #                               [0, 1, 0, 0, 0],
        #                               [1, 0, 1, 0, 0],
        #                               [0, 0, 0, 1, 0]], dtype=int)
        # self.vertices = 5

    def kosaraju(self) -> np.ndarray:
        """Use the Kosaraju's algorithm to find connected components in graph"""
        distance = np.full(self.vertices, -1, dtype=int)
        f = np.full(self.vertices, -1, dtype=int)
        t = 0
        for v in range(self.vertices):
            if distance[v] == -1:
                t, f = self.dfs_visit(v, distance, f, t)
        vertices_arr_transposed = self.edges_matrix.transpose()
        nr = 0
        comp = np.full(self.vertices, -1, dtype=int)
        arr = np.argsort(f)[::-1]
        for v in arr:
            if comp[v] == -1:
                nr += 1
                comp[v] = nr
                comp = self.components_r(nr, v, vertices_arr_transposed, comp)
        return comp

    def components_r(self, nr, v, matrix, comp) -> np.ndarray:
        """Set number of a component to vertex"""
        neighbors = self.neighbors(v, matrix)
        for neighbor in neighbors:
            if comp[neighbor] == -1:
                comp[neighbor] = nr
                comp = self.components_r(nr, neighbor, matrix, comp)
        return comp

    def dfs_visit(self, v, distance, f, t) -> (int, np.ndarray):
        """Deep-first search algorithm for digraph"""
        t += 1
        distance[v] = t
        neighbors = self.neighbors(v, self.edges_matrix)
        for neighbor in neighbors:
            if distance[neighbor] == -1:
                t, f = self.dfs_visit(neighbor, distance, f, t)
        t += 1
        f[v] = t
        return t, f

    def neighbors(self, vertex, matrix) -> list:
        """Return list of neighbors for given vertex in digraph"""
        neighbors = []
        for i, item in enumerate(matrix[vertex]):
            if item != 0:
                neighbors.append(i)
        return neighbors

    def strongly_connected_component(self) -> None:
        """Extract biggest strongly connected component from graph"""
        connected_components = self.kosaraju()
        components = np.unique(connected_components, return_counts=True)
        biggest_component = components[0][(np.argmax(components[1]))]
        unconnected_components = [i for i, item in enumerate(connected_components) if item != biggest_component]
        self.adjacency_matrix = np.delete(self.adjacency_matrix, unconnected_components, 0)
        self.adjacency_matrix = np.delete(self.adjacency_matrix, unconnected_components, 1)
        self.edges_matrix = np.delete(self.edges_matrix, unconnected_components, 0)
        self.edges_matrix = np.delete(self.edges_matrix, unconnected_components, 1)
        self.vertices = self.adjacency_matrix.shape[0]

    def bellman_ford(self, s) -> Union[np.ndarray, bool]:
        """Find distances to all vertices from starting vertex"""
        if s > self.vertices:
            raise IncorrectInputException("Starting vertex: " + s + " is bigger than size of the graph")
        d = np.full(self.vertices, np.inf)
        d[s] = 0
        vertices = np.empty(self.vertices, dtype=int)
        for i in range(self.vertices - 1):
            for j in range(self.vertices):
                for k in range(self.vertices):
                    if self.edges_matrix[j][k] != 0:
                        if d[k] > d[j] + self.adjacency_matrix[j][k]:
                            d[k] = d[j] + self.adjacency_matrix[j][k]
                            vertices[k] = j
        for i in range(self.vertices):
            for j in range(self.vertices):
                if self.edges_matrix[i][j] != 0:
                    if d[j] > d[i] + self.adjacency_matrix[i][j]:
                        return False
        return d, vertices

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
            [u_neighbours.append(i) if val != 0 else None for i, val in enumerate(self.edges_matrix[u])]

            distances, positions = self.relax_dijkstra(distances, positions, u, u_neighbours)

        return distances, positions

    def johnson(self) -> (bool, np.ndarray):
        temp_adjacency = self.adjacency_matrix
        self.vertices = self.vertices + 1
        matrix = np.zeros((self.vertices, self.vertices), int)
        matrix[1:self.vertices, 1:self.vertices] = self.adjacency_matrix
        self.adjacency_matrix = matrix

        matrix = np.zeros((self.vertices, self.vertices), int)
        matrix[1:self.vertices, 1:self.vertices] = self.edges_matrix
        matrix[0, 1:self.vertices] = np.ones((1, self.vertices - 1), int)
        self.edges_matrix = matrix
        w = np.zeros((self.vertices, self.vertices), int)
        h = []
        d = self.bellman_ford(0)
        if d:
            for v in range(self.vertices):
                h.append(d[0][v])
            for u in range(self.vertices):
                for v in range(self.vertices):
                    if self.edges_matrix[u][v] != 0:
                        w[u][v] = self.adjacency_matrix[u][v] + h[u] - h[v]
            self.adjacency_matrix = w[1:self.vertices, 1:self.vertices]
            self.edges_matrix = self.edges_matrix[1:self.vertices, 1:self.vertices]
            self.vertices = self.vertices - 1
            h = h[1:]
            D = np.zeros((self.vertices, self.vertices), int)
            for u in range(self.vertices):
                du, _ = self.dijkstra(u)
                for v in range(self.vertices):
                    D[u][v] = du[v] + h[v] - h[u]
            self.adjacency_matrix = temp_adjacency
            return True, D
        else:
            return False, []

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
        self.edges_matrix = np.zeros((vertices, vertices), dtype=int)
        for i in range(vertices):
            for j in range(vertices):
                if i != j:
                    r = random.random()
                    if r < probability and self.adjacency_matrix[j][i] == 0:
                        self.adjacency_matrix[i][j] = random.randint(a, b) if weight else 1
                        self.edges_matrix[i][j] = 1
        self.vertices = self.adjacency_matrix.shape[0]

    def set_digraph(self, data) -> None:
        """Sets the adjacency matrix"""
        graph, representation = data
        self.adjacency_matrix = GraphConverter.convert_graph(graph, representation,
                                                             GraphRepresentation.ADJACENCY_MATRIX)
        self.vertices = self.adjacency_matrix.shape[0]

    def __str__(self) -> str:
        """Returns the adjacency matrix"""
        return '\n'.join([' '.join([str(u) for u in row]) for row in self.adjacency_matrix])
