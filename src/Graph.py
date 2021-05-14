import math
from copy import deepcopy
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import random

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
        self.vertices = self.adjacency_matrix.shape[0]
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

    def randomize_graph_edges(self, number_of_randomizations):
        """
        Corner cases:
        - perform 100 randomizations,
        - random number of randomizations,
        - randomize graph where randomization is not possible (i. e. [3 3 3 3] or [2 2 2]).
        Perform number_of_randomizations randomizations and return True if operation succeeded.
        :param number_of_randomizations: number of randomizations to perform, if 0 the number should be random
        :return: True if randomization succeeded, False otherwise
        """
        adjacency_list = GraphConverter.convert_adj_mat_to_adj_list(self.adjacency_matrix)
        adjacency_list_copy = deepcopy(adjacency_list)
        flattened_list = [item for sublist in adjacency_list for item in sublist]

        # 3 or less vertices - to few to randomize
        if len(adjacency_list) <= 3:
            return False

        # draw number of randomization, because one wasn't specified
        if number_of_randomizations == 0:
            number_of_randomizations = random.randint(1, 100)

        # estimate number or randomizations that is possible to perform
        free_edges_counter = 0
        n = len(adjacency_list)
        for i in adjacency_list:
            free_edges_counter += n - 1 - len(i)
        free_edges_counter /= 2

        performed_randomizations = 0
        fails = 0

        while performed_randomizations < number_of_randomizations:
            [performed_randomizations, fails] = self.randomize(adjacency_list_copy, flattened_list,
                                                               performed_randomizations, fails, free_edges_counter)
        if performed_randomizations == fails:
            return False
        else:
            print("Randomizations performed: " + str(performed_randomizations - fails))
            self.adjacency_matrix = GraphConverter.convert_adj_list_to_adj_mat(adjacency_list_copy)
            return True

    @staticmethod
    def randomize(adjacency_list_copy, flattened_list, performed_randomizations, fails, free_edges_counter):
        """
        Randomize graph. Increment fails value if randomization fails.
        :param adjacency_list_copy: deepcopy of adjacency list
        :param flattened_list: flat list made from adjacency_list for drawing nodes
        :param performed_randomizations: number of tried randomizations
        :param fails: number of failed randomizations (either drawing eligible nodes took to long or randomization is not possible)
        :param free_edges_counter: number of possible randomizations in one go
        :return: updated values of performed randomizations and fails
        """
        # check if we didn't fall into an endless loop
        endless_loop_flag = 0

        # if we still should perform randomizing or didn't fall into endless loop
        while endless_loop_flag <= free_edges_counter * 4:
            first_start, first_end, second_start, second_end = random.sample(list(set(flattened_list)), k=4)

            # random nodes aren't connected in a way that would prevent randomizing (when one node is connected to two other)
            if (first_start in adjacency_list_copy[first_end - 1]) and (
                    second_start in adjacency_list_copy[second_end - 1]):
                if (first_start not in adjacency_list_copy[second_end - 1]) and (
                        second_start not in adjacency_list_copy[first_end - 1]):
                    # remove existing connections
                    adjacency_list_copy[first_start - 1].remove(first_end)
                    adjacency_list_copy[first_end - 1].remove(first_start)
                    adjacency_list_copy[second_start - 1].remove(second_end)
                    adjacency_list_copy[second_end - 1].remove(second_start)

                    # add new connections
                    adjacency_list_copy[first_start - 1].append(second_end)
                    adjacency_list_copy[second_end - 1].append(first_start)
                    adjacency_list_copy[second_start - 1].append(first_end)
                    adjacency_list_copy[first_end - 1].append(second_start)
                    return [performed_randomizations + 1, fails]

                # other randomization is possible
                elif (first_start not in adjacency_list_copy[second_start - 1]) and (
                        second_end not in adjacency_list_copy[first_end - 1]):
                    adjacency_list_copy[first_start - 1].remove(first_end)
                    adjacency_list_copy[first_end - 1].remove(first_start)
                    adjacency_list_copy[second_start - 1].remove(second_end)
                    adjacency_list_copy[second_end - 1].remove(second_start)

                    adjacency_list_copy[first_start - 1].append(second_start)
                    adjacency_list_copy[second_start - 1].append(first_start)
                    adjacency_list_copy[second_end - 1].append(first_end)
                    adjacency_list_copy[first_end - 1].append(second_end)
                    return [performed_randomizations + 1, fails]
            endless_loop_flag += 1

        return [performed_randomizations + 1, fails + 1]

    def set_graph(self, data) -> None:
        """Sets the adjacency matrix"""
        graph, representation = data
        self.adjacency_matrix = GraphConverter.convert_graph(graph, representation,
                                                             GraphRepresentation.ADJACENCY_MATRIX)
        self.vertices = self.adjacency_matrix.shape[0]

    def __str__(self) -> str:
        """Returns the adjacency matrix"""
        return '\n'.join([' '.join([str(u) for u in row]) for row in self.adjacency_matrix])

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
            if self.adjacency_matrix[start][i] == 1 and not visited[i]:
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

    # prints connected components, takes result of 'find components' method as an argument
    @staticmethod
    def print_components(comp) -> None:
        """
        Prints all connected components in a neat way and finds the biggest one
        :param comp: a list returned from find_components function
        :return:
        """
        cc_lengths = []
        searchval = 1
        while True:
            connected_comp = [x + 1 for x in np.where(comp == searchval)[0]]
            if len(connected_comp) == 0:
                break
            cc_lengths.append(len(connected_comp))
            print("{}) ".format(searchval), end='')
            print(*connected_comp)
            searchval += 1

        m = max(cc_lengths)
        indices = [i + 1 for i, j in enumerate(cc_lengths) if j == m]
        print("The biggest connected component has number ", end='')
        print(*indices)
