import unittest

import numpy as np

from Graph import Graph


class RandomizationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.gr = Graph()
        self.gr.adjacency_matrix = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

    def test_randomizing_random_times(self):
        self.assertEqual(self.gr.randomize_graph_edges(0), True)

    def test_randomizing_100_times(self):
        self.assertEqual(self.gr.randomize_graph_edges(100), True)

    def test_randomizing_too_small_graph(self):
        gr = Graph()
        gr.adjacency_matrix = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=int)
        self.assertEqual(gr.randomize_graph_edges(3), False)


if __name__ == '__main__':
    unittest.main()