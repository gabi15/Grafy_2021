import numpy as np
from GraphRepresentation import GraphRepresentation
from GraphConverter import GraphConverter


class IncorrectInputException(Exception):
    """Exception raised in case of bad input"""

    def __init__(self, message):
        self.message = message


class GraphReader:
    filename = None

    def read_data(self, representation, filename):
        self.filename = "./../data/" + filename
        if representation == GraphRepresentation.ADJACENCY_MATRIX:
            return self.read_adjacency_matrix()
        if representation == GraphRepresentation.ADJACENCY_LIST:
            return self.read_adjacency_list()
        if representation == GraphRepresentation.INCIDENCE_MATRIX:
            return self.read_incidence_matrix()
        if representation == GraphRepresentation.GRAPHICAL_SEQUENCE:
            return self.read_graphical_sequence()

    @staticmethod
    def is_square(matrix):
        return all(len(row) == len(matrix) for row in matrix)

    def read_adjacency_matrix(self):
        try:
            matrix = np.loadtxt(self.filename)
        except Exception as e:
            raise IncorrectInputException("Incorrect input - an error occurred while reading the file:\n" + str(e))
        if self.is_square(matrix):
            return matrix
        else:
            raise IncorrectInputException("Incorrect input - adjacency matrix built from input is not square")

    @staticmethod
    def is_symmetrical(matrix):
        transpose_matrix = matrix.transpose()
        comparison = transpose_matrix == matrix
        return comparison.all()

    def read_incidence_matrix(self):
        try:
            incidence_matrix = np.loadtxt(self.filename)
        except Exception as e:
            raise IncorrectInputException("Incorrect input - an error occurred while reading the file:\n" + str(e))
        matrix = GraphConverter().convert_graph(incidence_matrix, GraphRepresentation.INCIDENCE_MATRIX, GraphRepresentation.ADJACENCY_MATRIX)
        if matrix is not None:
            if self.is_symmetrical(matrix):
                return matrix
            else:
                raise IncorrectInputException("Incorrect input - adjacency matrix built from input is not symmetrical")
        else:
            raise IncorrectInputException("Incorrect input - column of the input matrix should contain two values")

    def read_adjacency_list(self):
        adjacency_list = []
        try:
            with open(self.filename) as f:
                for line in f:
                    row = [int(item.strip()) for item in line.split(" ") if line.strip()]
                    adjacency_list.append(row)
        except Exception as e:
            raise IncorrectInputException("Incorrect input - an error occurred while reading the file:\n" + str(e))
        matrix = GraphConverter().convert_graph(adjacency_list, GraphRepresentation.ADJACENCY_LIST, GraphRepresentation.ADJACENCY_MATRIX)
        if matrix:
            if self.is_symmetrical(matrix):
                return matrix
            else:
                raise IncorrectInputException("Incorrect input - adjacency matrix built from input is not symmetrical")
        raise IncorrectInputException("Incorrect input - List index is bigger than the number of vertices")

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
            return GraphConverter.convert_graph(GraphConverter().convert_graph(graphical_sequence[0], GraphRepresentation.GRAPHICAL_SEQUENCE, GraphRepresentation.ADJACENCY_LIST), GraphRepresentation.ADJACENCY_LIST, GraphRepresentation.ADJACENCY_MATRIX)
