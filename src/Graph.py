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
        self.vertices = -1

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

    def visualize_graph_with_weights(self, save_to_file, file_name) -> None:
        """Visualize weighted graph"""
        G = nx.from_numpy_matrix(np.matrix(self.adjacency_matrix), create_using=nx.DiGraph)
        layout = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw(G, layout, with_labels=True)
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)

        if save_to_file:
            plt.rcParams['savefig.format'] = 'png'
            plt.savefig("data/" + file_name)
        else:
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

    def find_center(self) -> int:
        """Find the node that has the smallest sum of distances to other nodes"""
        distances_matrix = self.find_distances_matrix()
        min_sum = sum(distances_matrix[0])
        current_index = 0
        node_index = 0

        for i in distances_matrix:
            if sum(i) < min_sum:
                min_sum = sum(i)
                node_index = current_index
            current_index += 1

        return node_index

    def find_minimax_center(self) -> int:
        """Find the node that has the smallest distance to the most distant node"""
        distances_matrix = self.find_distances_matrix()
        min_max = max(distances_matrix[0])
        current_index = 0
        node_index = 0

        for i in distances_matrix:
            if max(i) < min_max:
                min_max = max(i)
                node_index = current_index
            current_index += 1

        return node_index

    def DFS(self, start, visited, visited_collected) -> None:
        """
        Runs Depth First Search algorithm
        :param start: starting node
        :param visited: list needed to recursively call function
        :param visited_collected: list of visited nodes
        :return:
        """
        # add current node
        visited_collected.append(start)

        # Set current node as visited
        visited[start] = True

        # For every node of the graph
        for i in range(self.vertices):

            # If some node is adjacent to the current node and it has not already been visited
            if self.adjacency_matrix[start][i] > 0 and not visited[i]:
                self.DFS(i, visited, visited_collected)

    def find_components(self) -> np.ndarray:
        """
        finds connected components in graph and returns a list: for example [0,0,1] means that vertices
        0 and 1 are connected, vertex 3 is alone to work properly graph must have adjacency matrix initialized
        :return: list of connected components
        """
        nr = 0
        comp = np.zeros((self.vertices,), dtype=int)  # this will save
        for i in range(self.vertices):
            visited_collected = []
            if comp[i] == 0:
                nr += 1
                comp[i] = nr
                visited = [False] * self.vertices
                self.DFS(i, visited, visited_collected)
                for el in visited_collected:
                    comp[el] = nr
        return comp

    def set_graph(self, data) -> None:
        """Sets the adjacency matrix"""
        graph, representation = data
        self.adjacency_matrix = GraphConverter.convert_graph(graph, representation,
                                                             GraphRepresentation.ADJACENCY_MATRIX)
        self.vertices = self.adjacency_matrix.shape[0]

    def __str__(self) -> str:
        """Returns the adjacency matrix"""
        return '\n'.join([' '.join([str(u) for u in row]) for row in self.adjacency_matrix])
