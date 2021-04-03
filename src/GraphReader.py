import numpy as np
from GraphRepresentation import GraphRepresentation
from GraphConverter import GraphConverter


class GraphReader:
    filename = None

    def read_data(self, representation, filename):
        self.filename = "../data/" + filename
        if representation == GraphRepresentation.ADJACENCY_MATRIX:
            return self.read_adjacency_matrix()
        if representation == GraphRepresentation.ADJACENCY_LIST:
            return self.read_adjacency_list()
        if representation == GraphRepresentation.INCIDENCE_MATRIX:
            return self.read_incidence_matrix()

    def is_square(self, matrix):
        return all(len(row) == len(matrix) for row in matrix)

    def read_adjacency_matrix(self):
        try:
            matrix = np.loadtxt(self.filename)
        except:
            return False
        if self.is_square(matrix):
            return matrix
        else:
            print("Macierz nie jest kwadratowa - błędne dane wejściowe")
            return None

    def is_symmetrical(self, matrix):
        transpose_matrix = matrix.transpose()
        comparision = transpose_matrix == matrix
        return comparision.all()

    def read_incidence_matrix(self):
        try:
            incidence_matrix = np.loadtxt(self.filename)
        except:
            return None
        matrix = GraphConverter().convert_graph(incidence_matrix, GraphRepresentation.INCIDENCE_MATRIX, GraphRepresentation.ADJACENCY_MATRIX)
        if matrix is not None:
            if self.is_symmetrical(matrix):
                return matrix
            else:
                print("Macierz nie jest symetryczna - błędne dane wejściowe")
                return None
        print("Błędne dane wejściowe")
        return None


    def read_adjacency_list(self):
        adjacency_list = []
        with open(self.filename) as f:
            for line in f:
                row = [int(item.strip()) for item in line.split(" ") if line.strip()]
                adjacency_list.append(row)
        matrix = GraphConverter().convert_graph(adjacency_list, GraphRepresentation.ADJACENCY_LIST, GraphRepresentation.ADJACENCY_MATRIX)
        if matrix:
            if self.is_symmetrical(matrix):
                return matrix
            else:
                print("Macierz nie jest symetryczna - błędne dane wejściowe")
                return None
        print("Indeks listy wykracza poza ilość wierzchołków - błędne dane wejściowe")
        return None




