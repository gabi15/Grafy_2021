import unittest
from RandomGraphGenerator import *


class TestRandomGraphGenerator(unittest.TestCase):
    def test_random_graph_edges_bad_vertices(self):
        with self.assertRaises(BadNumberOfVertices):
            random_graph_edges(0, 4)

    def test_random_graph_edges_bad_edges(self):
        with self.assertRaises(BadNumberOfEdges):
            random_graph_edges(3, 7)

    def test_random_graph_edges(self):
        result = random_graph_edges(4, 3)[0]
        self.assertEqual(result.sum(), 6)
        self.assertEqual(result.shape, (4, 3))

    def test_random_graph_probability(self):
        n = 4
        p = 0.5
        result = random_graph_probability(n, p)[0]
        self.assertTrue(0 <= result.sum() // 2 <= (n * (n - 1)) // 2)
        self.assertEqual(result.diagonal().sum(), 0)
        self.assertEqual(result.shape, (n, n))

    def test_random_graph_probability_bad_vertices(self):
        with self.assertRaises(BadNumberOfVertices):
            random_graph_probability(0, 4)

    def test_random_graph_probability_bad_probability(self):
        with self.assertRaises(BadProbability):
            random_graph_probability(3, 7)
        with self.assertRaises(BadProbability):
            random_graph_probability(3, -7)

    def test_random_graph_regular_bad_vertices(self):
        with self.assertRaises(BadNumberOfVertices):
            random_graph_regular(0, 4)

    def test_random_graph_regular_bad_degree(self):
        with self.assertRaises(BadDegree):
            random_graph_regular(4, -7)
        with self.assertRaises(BadDegree):
            random_graph_regular(4, 4)

    def test_random_graph_regular_bad_values(self):
        with self.assertRaises(BadNKValues):
            random_graph_regular(5, 3)

    def test_random_graph_regular(self):
        n = 5
        k = 4
        result = random_graph_regular(n, k)[0]
        self.assertTrue(result.sum() == (n * k))
        self.assertEqual(result.diagonal().sum(), 0)
        self.assertEqual(result.shape, (n, n))


if __name__ == '__main__':
    unittest.main()
