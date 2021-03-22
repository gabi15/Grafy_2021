import numpy as np


class GraphReader:
    graph_matrix = None
    filename = None

    def __init__(self, option, filename):
        self.filename = filename
        self.option = option

    def read_input_data(self):
        if self.option == 1:
            return self.read_adjacency_matrix()
        if self.option == 2:
            return self.read_adjacency_list()
        if self.option == 3:
            return self.read_incidence_matrix()

    def is_square(self):
        return all(len(row) == len(self.graph_matrix) for row in self.graph_matrix)

    def read_adjacency_matrix(self):
        try:
            self.graph_matrix = np.loadtxt(self.filename)
        except:
            return False
        return self.is_square()

    def is_symmetrical(self, matrix):
        transpose_matrix = matrix.transpose()
        comparision = transpose_matrix == matrix
        return comparision.all()

    def read_incidence_matrix(self):
        try:
            incidence_matrix = np.loadtxt(self.filename)
        except:
            return False
        matrix_size = len(incidence_matrix)
        matrix = np.zeros((matrix_size, matrix_size), np.int8)
        for column in incidence_matrix.transpose():
            edge = []
            for i, item in enumerate(column):
                if item == 1:
                    edge.append(i)
            if len(edge) != 2:
                return False
            matrix[edge[0]][edge[1]] = 1
            matrix[edge[1]][edge[0]] = 1
        if self.is_symmetrical(matrix):
            self.graph_matrix = matrix
            print(self.graph_matrix)
            return True
        else:
            return False

    def read_adjacency_list(self):
        adjacency_list = []
        with open(self.filename) as f:
            for line in f:
                row = [int(item.strip()) for item in line.split(" ")]
                adjacency_list.append(row)
        matrix_size = len(adjacency_list)
        matrix = np.zeros((matrix_size, matrix_size), np.int8)
        try:
            for i, row in enumerate(adjacency_list):
                for item in row:
                    matrix[i][item-1] = 1
        except:
            return False
        if self.is_symmetrical(matrix):
            self.graph_matrix = matrix
            return True
        else:
            return False




