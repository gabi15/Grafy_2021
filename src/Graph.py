from src.GraphReader import GraphReader
from src.GraphConverter import GraphConverter
import numpy as np

class Graph:
    graph_reader = GraphReader()
    graph_converter = GraphConverter()
    adjacency_matrix = None

    def read_data(self, representation, filename):
        self.adjacency_matrix = self.graph_reader.read_data(representation, filename)

    def get_graph(self, representation):
        return self.graph_converter.convert_graph(self.adjacency_matrix, representation)

    def save_to_file(self, representation, filename):
        output_matrix = self.get_graph(representation)
        if isinstance(output_matrix, list):
            with open(filename, "w") as f:
                for row in output_matrix:
                    f.write(" ".join(str(item) for item in row))
                    f.write("\n")
            return True
        elif isinstance(output_matrix, np.ndarray):
            np.savetxt(filename, output_matrix, fmt="%i")
            return True
        else:
            return False

    def print_graph_matrix(self):
        print(self.adjacency_matrix)
