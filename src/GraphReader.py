import numpy as np
from GraphRepresentation import GraphRepresentation
from GraphConverter import GraphConverter


class IncorrectInputException(Exception):
    """Exception raised in case of bad input"""

    def __init__(self, message):
        self.message = message


class GraphReader:
    filename = None

    def read_data(self, representation, filename) -> np.ndarray:
        """Read a graph from a file using given representation"""
        self.filename = "data/" + filename
        if representation == GraphRepresentation.ADJACENCY_MATRIX:
            return self.read_adjacency_matrix()
        if representation == GraphRepresentation.ADJACENCY_LIST:
            return self.read_adjacency_list()
        if representation == GraphRepresentation.INCIDENCE_MATRIX:
            return self.read_incidence_matrix()

    @staticmethod
    def is_square(matrix) -> bool:
        """Check if a matrix is square"""
        return all(len(row) == len(matrix) for row in matrix)

    @staticmethod
    def is_symmetrical(matrix) -> bool:
        """Check if the matrix is symmetrical"""
        transpose_matrix = matrix.transpose()
        comparision = transpose_matrix == matrix
        return comparision.all()

    def read_adjacency_matrix(self) -> np.ndarray:
        """Read an adjacency matrix from a file"""
        try:
            matrix = np.loadtxt(self.filename)
        except Exception as e:
            raise IncorrectInputException("Incorrect input - an error occurred while reading the file:\n" + str(e))
        if self.is_square(matrix):
            return matrix
        else:
            raise IncorrectInputException("Incorrect input - adjacency matrix built from input is not square")

    def read_incidence_matrix(self) -> np.ndarray:
        """Read an incidence matrix from a file"""
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

    def read_adjacency_list(self) -> np.ndarray:
        """Read an adjacency list from a file"""
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




