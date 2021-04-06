from GraphRepresentation import GraphRepresentation
import numpy as np


class GraphConverter:

    @staticmethod
    def convert_graph(graph, input_representation, output_representation):
        if input_representation == GraphRepresentation.ADJACENCY_MATRIX:
            return GraphConverter.convert_from_adjacency_matrix(graph, output_representation)
        elif input_representation == GraphRepresentation.ADJACENCY_LIST:
            return GraphConverter.convert_from_adjacency_list(graph, output_representation)
        elif input_representation == GraphRepresentation.INCIDENCE_MATRIX:
            return GraphConverter.convert_from_incidence_matrix(graph, output_representation)

    @staticmethod
    def convert_from_adjacency_matrix(graph, output_representation):
        if output_representation == GraphRepresentation.ADJACENCY_MATRIX:
            return graph
        elif output_representation == GraphRepresentation.ADJACENCY_LIST:
            return GraphConverter.convert_adj_mat_to_adj_list(graph)
        elif output_representation == GraphRepresentation.INCIDENCE_MATRIX:
            return GraphConverter.convert_adj_mat_to_inc_mat(graph)

    @staticmethod
    def convert_from_adjacency_list(adjacency_list, output_representation):
        if output_representation == GraphRepresentation.ADJACENCY_MATRIX:
            return GraphConverter.convert_adj_list_to_adj_mat(adjacency_list)
        elif output_representation == GraphRepresentation.ADJACENCY_LIST:
            return adjacency_list
        elif output_representation == GraphRepresentation.INCIDENCE_MATRIX:
            return GraphConverter.convert_adj_list_to_inc_mat(adjacency_list)

    @staticmethod
    def convert_from_incidence_matrix(graph, output_representation):
        if output_representation == GraphRepresentation.ADJACENCY_MATRIX:
            return GraphConverter.convert_inc_mat_to_adj_mat(graph)
        elif output_representation == GraphRepresentation.ADJACENCY_LIST:
            return GraphConverter.convert_inc_mat_to_adj_list(graph)
        elif output_representation == GraphRepresentation.INCIDENCE_MATRIX:
            return graph

    @staticmethod
    def convert_adj_list_to_adj_mat(adjacency_list):
        matrix_size = len(adjacency_list)
        matrix = np.zeros((matrix_size, matrix_size), dtype=int)
        try:
            for i, row in enumerate(adjacency_list):
                for item in row:
                    matrix[i][item - 1] = 1
            return matrix
        except:
            return None

    @staticmethod
    def convert_inc_mat_to_adj_mat(incidence_matrix):
        matrix_size = len(incidence_matrix)
        matrix = np.zeros((matrix_size, matrix_size), dtype=int)
        for column in incidence_matrix.transpose():
            edge = []
            for i, item in enumerate(column):
                if item == 1:
                    edge.append(i)
            if len(edge) != 2:
                return None
            matrix[edge[0]][edge[1]] = 1
            matrix[edge[1]][edge[0]] = 1
        return matrix

    @staticmethod
    def convert_adj_mat_to_adj_list(graph):
        adjacency_list = []
        for row in graph:
            neighbors = []
            for i, item in enumerate(row):
                if item == 1:
                    neighbors.append(i+1)
            adjacency_list.append(neighbors)
        return adjacency_list

    @staticmethod
    def convert_adj_mat_to_inc_mat(graph):
        incidence_matrix = []
        row_length = graph[0].size
        for i, row in enumerate(graph):
            for j in range(i):
                if row[j] == 1:
                    edge = np.zeros(row_length, dtype=int)
                    edge[i] = 1
                    edge[j] = 1
                    incidence_matrix.append(edge)
        incidence_matrix = np.array(incidence_matrix).transpose()
        return incidence_matrix

    @staticmethod
    def convert_adj_list_to_inc_mat(adjacency_list):
        try:
            adjacency_list = GraphConverter.convert_adj_list_to_adj_mat(adjacency_list)
        except:
            return None
        return GraphConverter.convert_adj_mat_to_inc_mat(adjacency_list)

    @staticmethod
    def convert_inc_mat_to_adj_list(graph):
        try:
            graph = GraphConverter.convert_inc_mat_to_adj_mat(graph)
        except:
            return None
        return GraphConverter.convert_adj_mat_to_adj_list(graph)
