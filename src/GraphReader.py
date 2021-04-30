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

