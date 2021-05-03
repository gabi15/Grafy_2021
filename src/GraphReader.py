import warnings

import numpy as np

import GraphConverter
from GraphConverter import IncorrectInputException
from GraphConverter import has_zeros_on_diagonal
from GraphConverter import is_symmetrical
from GraphConverter import is_square
from GraphRepresentation import GraphRepresentation


class GraphReader:
    def __init__(self):
        self.filename = None

    def read_data(self, representation, filename) -> np.ndarray:
        """Read a graph from a file using given representation"""
        self.filename = "data/" + filename
        if representation == GraphRepresentation.ADJACENCY_MATRIX:
            return self.read_adjacency_matrix()
        if representation == GraphRepresentation.ADJACENCY_LIST:
            return self.read_adjacency_list()
        if representation == GraphRepresentation.INCIDENCE_MATRIX:
            return self.read_incidence_matrix()
        if representation == GraphRepresentation.GRAPHICAL_SEQUENCE:
            return self.read_graphical_sequence()

    def read_from_file(self) -> np.ndarray:
        """Read a matrix from a file"""
        warnings.filterwarnings("error")
        try:
            matrix = np.loadtxt(self.filename, dtype=int)
        except Exception as e:
            raise IncorrectInputException("an error occurred while reading the file:\n" + str(e))
        return matrix

    def read_adjacency_matrix(self) -> np.ndarray:
        """Read an adjacency matrix from a file"""
        matrix = self.read_from_file()
        if not is_square(matrix):
            raise IncorrectInputException("Adjacency matrix built from input is not square")
        if not is_symmetrical(matrix):
            raise IncorrectInputException("Adjacency matrix built from input is not symmetrical")
        if not has_zeros_on_diagonal(matrix):
            raise IncorrectInputException("Adjacency matrix built from input has non zero value on diagonal")
        return matrix

    def read_incidence_matrix(self) -> np.ndarray:
        """Read an incidence matrix from a file"""
        incidence_matrix = self.read_from_file()
        matrix = GraphConverter.convert_graph(incidence_matrix, GraphRepresentation.INCIDENCE_MATRIX,
                                              GraphRepresentation.ADJACENCY_MATRIX)
        return matrix

    def read_adjacency_list(self) -> np.ndarray:
        """Read an adjacency list from a file"""
        adjacency_list = []
        try:
            with open(self.filename) as f:
                for line in f:
                    row = [int(item.strip()) for item in line.split(" ") if line.strip()]
                    adjacency_list.append(row)
            if len(adjacency_list) == 0:
                raise Exception("file is empty")
        except Exception as e:
            raise IncorrectInputException("an error occurred while reading the file:\n" + str(e))
        matrix = GraphConverter.convert_graph(adjacency_list, GraphRepresentation.ADJACENCY_LIST,
                                              GraphRepresentation.ADJACENCY_MATRIX)
        return matrix

    def is_graphical_sequence(self, graphical_sequence):
        n = len(graphical_sequence)
        graph_seq = sorted(graphical_sequence, reverse=True)

        if sum(i % 2 for i in graph_seq) % 2 or graph_seq[n - 1] < 0 or graph_seq[0] >= n:
            return False

        flag = 0
        for i in range(0, n):
            if graph_seq[i] == 0:
                flag += 1
        if flag == n:
            return True

        for i in range(1, graph_seq[0] + 1):
            if graph_seq[i] > 0:
                graph_seq[i] -= 1
            else:
                return False
        graph_seq[0] = 0

        return self.is_graphical_sequence(graph_seq)

    def read_graphical_sequence(self):
        graphical_sequence = []
        try:
            with open(self.filename) as f:
                line = f.readline()
                elements = [int(item.strip()) for item in line.split(" ") if line.strip()]
                graphical_sequence.append(elements)
        except Exception as e:
            raise IncorrectInputException("Incorrect input - an error occurred while reading the file:\n" + str(e))
        if len(graphical_sequence) == 0:
            raise IncorrectInputException("Incorrect input - graphical sequence is empty")
        elif not self.is_graphical_sequence(graphical_sequence[0]):
            raise IncorrectInputException("Incorrect input - sequence is not graphical")
        else:
            return GraphConverter.convert_graph(GraphConverter.convert_graph(graphical_sequence[0], GraphRepresentation.GRAPHICAL_SEQUENCE, GraphRepresentation.ADJACENCY_LIST), GraphRepresentation.ADJACENCY_LIST, GraphRepresentation.ADJACENCY_MATRIX)
