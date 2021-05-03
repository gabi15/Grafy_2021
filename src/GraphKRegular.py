import numpy as np
import random
from RandomGraphGenerator import BadNumberOfVertices

class BadNKValues(Exception):
    """Raised when number of degrees is bigger than the number of vertices """

class BadNumberofDegrees(Exception):
    """Raised when number of degrees is less than 1 """

class GraphKRegular:
    @staticmethod
    def generate_k_regular(n, k):
        """Generate adjacency matrix for a k-regular graph with n vertices"""

        if n < 2:
            raise BadNumberOfVertices
        if k > n:
            raise BadNKValues
        if k < 1:
            raise BadNumberofDegrees

        matrix = np.zeros((n, n), dtype=int)

        # more complicated version 
        # while np.sum(matrix) != n * k:
            # temp = np.where(matrix==0)
            # S = list(zip(temp[0], temp[1]))
            # pairs = []
            # for i, j in S:
            #     if i!=j:
            #         d_i = np.sum(matrix[:, i])
            #         d_j = np.sum(matrix[:, j])
            #         if d_i < k and d_j < k:
            #             pairs.append([(i,j), (k-d_i)*(k-d_j)])
            # u,v = random.choices([x[0] for x in pairs], cum_weights=[x[1] for x in pairs])[0]
            # matrix[u][v] = matrix[v][u] = 1

        U = [i for i in range(n*k)]
        pairs = []
        while len(U)>0:
            u, v = random.choices(U, k = 2)
            if u!=v:
                pairs.append((u,v))
                U.remove(u)
                U.remove(v)
        for u,v in pairs:
            matrix[u%n][v%n] = matrix[v%n][u%n] = 1

        # randomize_graph_edges???
        return matrix