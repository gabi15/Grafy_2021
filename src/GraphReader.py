import warnings

import numpy as np

from Digraph import IncorrectInputException


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
