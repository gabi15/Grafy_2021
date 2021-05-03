import unittest
from GraphChecking import *


class TestGraphChecking(unittest.TestCase):
    def setUp(self) -> None:
        self.good_hamiltonian_graph = np.array([[0, 1, 1, 1, 1],
                                                [1, 0, 1, 0, 1],
                                                [1, 1, 0, 1, 1],
                                                [1, 0, 1, 0, 0],
                                                [1, 1, 1, 0, 0]], dtype=int)
        self.bad_hamiltonian_graph = np.array([[0, 1, 0, 0],
                                               [1, 0, 1, 1],
                                               [0, 1, 0, 0],
                                               [0, 1, 0, 0]], dtype=int)

    def test_good_hamiltonian(self):
        self.assertTrue(hamiltonian(self.good_hamiltonian_graph)[0])

    def test_bad_hamiltonian(self):
        self.assertFalse(hamiltonian(self.bad_hamiltonian_graph)[0])

    def test_hamiltonian_bad_start(self):
        with self.assertRaises(BadStartNode):
            hamiltonian(self.good_hamiltonian_graph, -7)
        with self.assertRaises(BadStartNode):
            hamiltonian(self.good_hamiltonian_graph, 7)


if __name__ == '__main__':
    unittest.main()
