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
    
    def test_random_graph_probability(self):
        with self.assertRaises(BadNumberOfVertices):
            RandomGraphGenerator.random_graph_probability(0, 4)
        with self.assertRaises(BadProbability):
            RandomGraphGenerator.random_graph_probability(3, 7)
        with self.assertRaises(BadProbability):
            RandomGraphGenerator.random_graph_probability(3, -7)
        n = 4
        p = 0.5
        result = RandomGraphGenerator.random_graph_probability(n, p)
        self.assertTrue(0<=result.sum()//2<=(n*(n-1))//2)
        self.assertEqual(result.diagonal().sum(), 0)
        self.assertEqual(result.shape, (n, n))

if __name__ == '__main__':
    unittest.main()
