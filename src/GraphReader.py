import warnings

import numpy as np

from GraphConverter import IncorrectInputException


class GraphReader:
    def __init__(self):
        self.filename = None

    def read_data(self, filename) -> np.ndarray:
        """Read a matrix from a file"""
        filename = "data/" + filename
        try:
            matrix = np.loadtxt(filename, dtype=int)
        except Exception as e:
            raise IncorrectInputException("an error occurred while reading the file:\n" + str(e))
        return matrix
