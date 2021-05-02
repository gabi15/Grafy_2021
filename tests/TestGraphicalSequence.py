import unittest

from GraphReader import GraphReader, IncorrectInputException


class TestGraphicalSequence(unittest.TestCase):

    def test_reading_empty_graph_seq(self):
        gr = GraphReader()
        gr.filename = "test_data/empty_graph_seq.txt"
        with self.assertRaises(IncorrectInputException):
            GraphReader.read_graphical_sequence(gr)

    def test_reading_wrong_graph_seq(self):
        gr = GraphReader()
        gr.filename = "test_data/wrong_graph_seq.txt"
        with self.assertRaises(IncorrectInputException):
            GraphReader.read_graphical_sequence(gr)

    def test_proper_single_elem_graph_seq(self):
        gr = GraphReader()
        self.assertEqual(gr.is_graphical_sequence([0]), True)

    def test_wrong_single_elem_graph_seq(self):
        gr = GraphReader()
        self.assertEqual(gr.is_graphical_sequence([2]), False)

    def test_proper_graph_seq(self):
        gr = GraphReader()
        self.assertEqual(gr.is_graphical_sequence([2, 2, 2]), True)

    def test_wrong_graph_seq(self):
        gr = GraphReader()
        self.assertEqual(gr.is_graphical_sequence([3, 2, 2]), False)

    def test_proper_all_zeros_graph_seq(self):
        gr = GraphReader()
        self.assertEqual(gr.is_graphical_sequence([0, 0, 0, 0]), True)


if __name__ == '__main__':
    unittest.main()
