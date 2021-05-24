import warnings

import numpy as np

class IncorrectInputException(Exception):
    """Exception raised in case of bad input"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Incorrect input - " + self.message


class GraphReader:
    def __init__(self):
        self.filename = None

    def read_data(self, filename_edges) -> np.ndarray:
        """Read a matrix from a file"""
        warnings.filterwarnings("error")
        try:
            matrix = np.loadtxt(self.filename, dtype=int)
        except Exception as e:
            raise IncorrectInputException("an error occurred while reading the file:\n" + str(e))
        return matrix
