import numpy as np
import random
from src.random_graph_edges import BadNumberOfEdges

class BadProbability(Exception):
    """Raised when value of probability is less than 0 or more than 1 """

def random_graph_probability(n, p): # creates a graph using the incidence matrix
    matrix = np.zeros((n, n), dtype=int)

    for i in range(n): 
        for j in range(i+1, n): 
            r = random.random() 
            if (r < p): 
                matrix[i][j] = matrix [j][i] = 1

    return matrix

def random_probability_to_file(n, p, filename):
    try:
        if n < 2:
            raise BadNumberOfVertices
        if p > 1 or p < 0:
            raise BadProbability
    except BadNumberOfVertices:
        print("number of vertices must be bigger than 1")
        return 0
    except BadProbability:
        print("probability must be between 0 and 1")
        return 0

    result = random_graph_probability(n, p)

    with open(filename,'w') as file: # Use file to refer to the file object
        for row in result:
            for el in row:
                file.write(str(el)+' ')
            file.write('\n')

# example
# input_n = 5
# input_p = 0.4
# random_probability_to_file(input_n,input_p, 'result.txt')