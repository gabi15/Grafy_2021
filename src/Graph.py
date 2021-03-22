from src.GraphReader import GraphReader
from src.GraphConverter import GraphConverter


class Graph:
    adjacency_matrix = None
    graph_reader = GraphReader()
    graph_converter = GraphConverter()

    def read_data(self, representation, filename):
        self.adjacency_matrix = self.graph_reader.read_data(representation, filename)

    def get_graph(self, representation):
        return self.graph_converter.convert_graph(self.adjacency_matrix, representation)

    def print_graph_matrix(self):
        print(self.adjacency_matrix)
