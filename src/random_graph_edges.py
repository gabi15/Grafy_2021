import numpy as np
import random


class BadNumberOfEdges(Exception):
    """Raised when number of Edges is too big """

class BadNumberOfVertices(Exception):
    """Raised when number of vertices is smaller than 2 """


def random_graph(n, m):
    matrix = np.zeros((n, m), dtype=int)
    i=0
    while i < m:
        first_rand = random.randint(0, n - 1)
        second_rand = random.randint(0, n - 1)
        while first_rand == second_rand:
            second_rand = random.randint(0, n - 1)
        is_duplicated = False
        for j in range(i):
            if matrix[first_rand][j] == 1 and matrix[second_rand][j] == 1:
                is_duplicated = True
                break

        if not is_duplicated:
            matrix[first_rand][i] = 1
            matrix[second_rand][i] = 1
            i += 1
    return matrix


def random_to_file(n, m, filename):
    try:
        if n < 2:
            raise BadNumberOfVertices
        if m > n*(n-1)/2 or m <= 0:
            raise BadNumberOfEdges
    except BadNumberOfVertices:
        print("number of edges and vertices must be bigger than 1")
        return 0
    except BadNumberOfEdges:
        print("enter correct number of edges please")
        return 0
    result = random_graph(n, m)
    with open(filename,'w') as file: # Use file to refer to the file object
        for row in result:
            for el in row:
                file.write(str(el)+' ')
            file.write('\n')

#usage
# input_n = 5
# input_m = 7
# random_to_file(input_n,input_m, 'result.txt')