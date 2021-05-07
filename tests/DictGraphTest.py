import unittest
from DictGraph import *


class TestDictGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = DictGraph([[2, 3], [1, 4], [1, 4], [2, 3]])

    def test_add_edge(self):
        self.graph.add_edge(1, 4)
        self.assertIn(4, self.graph.adjacency_dict[1])

    def test_remove_edge(self):
        self.graph.remove_edge(1, 2)
        self.assertNotIn(2, self.graph.adjacency_dict[1])

    def test_valid_edge(self):
        self.assertTrue(self.graph.is_next_edge_valid(1, 2))

    def test_DFS_count(self):
        visited = [False]*5
        count = self.graph.DFS_count(1, visited)
        self.assertEqual(count,4)

    def test_find_euler_cycle(self):
        edges = []
        edges = self.graph.find_euler_cycle(1, edges)
        self.assertEqual(len(edges), 4)

    def test_random_even_graphical_sequence(self):
        sequence = random_even_graphical_sequence(5)
        self.assertNotIn(1,sequence)
        self.assertNotIn(3, sequence)
        self.assertNotIn(6, sequence)
        self.assertEqual(len(sequence), 5)

    def test_random_euler_graph(self):
        adj_list = random_euler_graph(7)
        self.assertEqual(len(adj_list), 7)


if __name__ == '__main__':
    unittest.main()
