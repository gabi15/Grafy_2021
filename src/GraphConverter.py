from src.GraphRepresentation import GraphRepresentation
import numpy as np


class GraphConverter:

    def convert_graph(self, graph, representation):
        if representation == GraphRepresentation.ADJACENCY_MATRIX:
            return self.convert_to_adjacency_matrix(graph)
        elif representation == GraphRepresentation.ADJACENCY_LIST:
            return self.convert_to_adjacency_list(graph)
        elif representation == GraphRepresentation.INCIDENCE_MATRIX:
            return self.convert_to_incidence_matrix(graph)

    def convert_to_adjacency_matrix(self, graph):
        return graph

    def convert_to_adjacency_list(self, graph):
        adjacency_list = []
        for row in graph:
            neighbors = []
            for i, item in enumerate(row):
                if item == 1:
                    neighbors.append(i+1)
            adjacency_list.append(neighbors)
        return adjacency_list

    def convert_to_incidence_matrix(self, graph):
        incidence_matrix = []
        row_length = graph[0].size
        for i, row in enumerate(graph):
            for j in range(i):
                if row[j] == 1:
                    edge = np.zeros(row_length, np.uint8)
                    edge[i] = 1
                    edge[j] = 1
                    incidence_matrix.append(edge)
        incidence_matrix = np.array(incidence_matrix).transpose()
        return incidence_matrix
        # return np.array([[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        #                 [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        #                 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        #                 [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]])


