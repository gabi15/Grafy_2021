import unittest
from RandomGraphGenerator import RandomGraphGenerator, BadNumberOfEdges, BadNumberOfVertices, BadProbability


class TestRandomGraphGenerator(unittest.TestCase):
    def test_random_graph_edges(self):
        with self.assertRaises(BadNumberOfVertices):
            RandomGraphGenerator.random_graph_edges(0, 4)
        with self.assertRaises(BadNumberOfEdges):
            RandomGraphGenerator.random_graph_edges(3, 7)
        result = RandomGraphGenerator.random_graph_edges(4, 3)
        self.assertEqual(result.sum(), 6)
        self.assertEqual(result.shape, (4, 3))


if __name__ == '__main__':
    unittest.main()
