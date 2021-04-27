import unittest

from GraphReader import *
from GraphRepresentation import GraphRepresentation


class ReadAdjacencyMatrixTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.reader = GraphReader()
        self.graph = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
                               [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                               [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                               [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]], dtype=int)

    def test_wrong_size_mat(self):
        with self.assertRaises(IncorrectInputException):
            self.reader.read_data(GraphRepresentation.ADJACENCY_MATRIX, "test_data/wrong_size_adj_mat.txt")

    def test_empty_file(self):
        with self.assertRaises(IncorrectInputException):
            self.reader.read_data(GraphRepresentation.ADJACENCY_MATRIX, "test_data/emptyfile.txt")

    def test_not_square_mat(self):
        expected = "Incorrect input - adjacency matrix built from input is not square or it has non zero values on the diagonal"

        with self.assertRaises(IncorrectInputException) as ctx:
            self.reader.read_data(GraphRepresentation.ADJACENCY_MATRIX, "test_data/not_square_adj_mat.txt")
        self.assertEqual(expected, str(ctx.exception), "Messages are not equal")

    def test_non_zero_on_diagonal(self):
        expected = "Incorrect input - adjacency matrix built from input is not square or it has non zero values on the diagonal"

        with self.assertRaises(IncorrectInputException) as ctx:
            self.reader.read_data(GraphRepresentation.ADJACENCY_MATRIX, "test_data/non_zero_on_diag.txt")
        self.assertEqual(expected, str(ctx.exception), "Messages are not equal")

    def test_one_val_in_file(self):
        expected = "Incorrect input - adjacency matrix built from input is not square or it has non zero values on the diagonal"

        with self.assertRaises(IncorrectInputException) as ctx:
            self.reader.read_data(GraphRepresentation.ADJACENCY_MATRIX, "test_data/one.txt")
        self.assertEqual(expected, str(ctx.exception), "Messages are not equal")

        self.assertEqual(0, self.reader.read_data(GraphRepresentation.ADJACENCY_MATRIX, "test_data/zero.txt"))

    def test_read_correct_mat(self):
        self.assertTrue(np.array_equal(self.graph, self.reader.read_data(GraphRepresentation.ADJACENCY_MATRIX,
                                                                         "test_data/generated.txt")))


class ReadIncidenceMatrixTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.reader = GraphReader()
        self.graph = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
                               [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                               [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                               [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]], dtype=int)

    def test_empty_file(self):
        with self.assertRaises(IncorrectInputException):
            self.reader.read_data(GraphRepresentation.INCIDENCE_MATRIX, "test_data/emptyfile.txt")

    def test_wrong_column_inc_mat(self):
        expected = "Incorrect input - column of the input matrix should contain two values"

        with self.assertRaises(IncorrectInputException) as ctx:
            self.reader.read_data(GraphRepresentation.INCIDENCE_MATRIX, "test_data/three_vals_in_col_inc_mat.txt")
        self.assertEqual(expected, str(ctx.exception), "Messages are not equal")

    def test_read_correct_input_mat(self):
        self.assertTrue(np.array_equal(self.graph, self.reader.read_data(GraphRepresentation.INCIDENCE_MATRIX,
                                                                         "test_data/generated_inc_mat.txt")))


class ReadAdjacencyListTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.reader = GraphReader()
        self.graph = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
                               [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                               [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                               [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                               [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]], dtype=int)

    def test_empty_file(self):
        with self.assertRaises(IncorrectInputException):
            self.reader.read_data(GraphRepresentation.ADJACENCY_LIST, "test_data/emptyfile.txt")

    def test_read_correct_input_list(self):
        self.assertTrue(np.array_equal(self.graph, self.reader.read_data(GraphRepresentation.ADJACENCY_LIST,
                                                                         "test_data/generated_adj_list.txt")))


if __name__ == '__main__':
    unittest.main()
