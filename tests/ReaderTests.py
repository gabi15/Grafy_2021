import unittest

from GraphReader import *
from GraphRepresentation import GraphRepresentation


class ReadAdjacencyMatrixTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.reader = GraphReader()

    def test_something(self):
        with self.assertRaises(IncorrectInputException) as ctx:
            self.reader.read_data(GraphRepresentation.ADJACENCY_MATRIX, "wrong_size_adj_mat.txt")


if __name__ == '__main__':
    unittest.main()
