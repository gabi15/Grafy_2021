import warnings

import numpy as np

import GraphConverter
from GraphRepresentation import GraphRepresentation


class IncorrectInputException(Exception):
    """Exception raised in case of bad input"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Incorrect input - " + self.message


def is_square(matrix) -> bool:
    """Check if a matrix is square"""
    if matrix.ndim == 0:
        return True
    elif matrix.ndim == 2:
        return matrix.shape[0] == matrix.shape[1]
    return False


def is_symmetrical(matrix) -> bool:
    """Check if the matrix is symmetrical"""
    transpose_matrix = matrix.transpose()
    comparision = transpose_matrix == matrix
    return comparision.all()


def has_zeros_on_diagonal(matrix) -> bool:
    """Check if the matrix has zeros on diagonal"""
    if matrix.ndim == 0:
        if matrix == 0:
            return True
        return False
    elif matrix.ndim == 2:
        for i, row in enumerate(matrix):
            if row[i] != 0:
                return False
        return True
    return False


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
        if is_square(matrix) and has_zeros_on_diagonal(matrix):
            return matrix
        else:
            raise IncorrectInputException(
                "adjacency matrix built from input is not square or it has non zero values on the diagonal")

    def read_incidence_matrix(self) -> np.ndarray:
        """Read an incidence matrix from a file"""
        incidence_matrix = self.read_from_file()
        matrix = GraphConverter.convert_graph(incidence_matrix, GraphRepresentation.INCIDENCE_MATRIX,
                                              GraphRepresentation.ADJACENCY_MATRIX)
        if matrix is not None:
            if is_symmetrical(matrix):
                return matrix
            else:
                raise IncorrectInputException("adjacency matrix built from input is not symmetrical")
        else:
            raise IncorrectInputException("column of the input matrix should contain two values")

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
        if matrix is not None:
            if is_symmetrical(matrix):
                return matrix
            else:
                raise IncorrectInputException("adjacency matrix built from input is not symmetrical")
        raise IncorrectInputException("list index is bigger than the number of vertices")
