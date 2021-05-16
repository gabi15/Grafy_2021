from Graph import *
from GraphRepresentation import *
from GraphConverter import convert_graph
from random import randrange


class DictGraph:
    def __init__(self, adj_list):
        self.adjacency_dict = {}
        for c, value in enumerate(adj_list, 1):
            self.adjacency_dict[c] = value
        self.vertices = len(adj_list)

    def add_edge(self, u, v) -> None:
        """
        Add edge to the graph
        :param u: first vertex number
        :param v: second vertex number
        :return:
        """
        self.adjacency_dict[u].append(v)
        self.adjacency_dict[v].append(u)

    # This function removes edge u-v from graph
    def remove_edge(self, u, v) -> None:
        """
        Remove edge from the graph
        :param u: first vertex number
        :param v: second vertex number
        :return:
        """
        for index, key in enumerate(self.adjacency_dict[u]):
            if key == v:
                self.adjacency_dict[u].pop(index)
        for index, key in enumerate(self.adjacency_dict[v]):
            if key == u:
                self.adjacency_dict[v].pop(index)

    def DFS_count(self, v, visited) -> int:
        """
        A DFS based function to count reachable vertices from v
        :param v: vertex from which we try to reach others
        :param visited: list passed between calls of function, on the first call filled with False
        :return:
        """
        count = 1
        visited[v] = True
        for i in self.adjacency_dict[v]:
            if not visited[i]:
                count = count + self.DFS_count(i, visited)
        return count

    def is_next_edge_valid(self, u, v) -> bool:
        """
        The function to check if edge u-v can be considered as next edge in Euler Cycle
        :param u: first vertex number
        :param v: second vertex number
        :return:
        """
        # The edge u-v is valid in one of the following two cases:

        #  1) If v is the only adjacent vertex of u
        if len(self.adjacency_dict[u]) == 1:
            return True
        else:
            '''
             2) If there are multiple adjacents, then u-v is not a bridge
                 Do following steps to check if u-v is a bridge

            2.a) count of vertices reachable from u'''
            visited = [False] * (self.vertices + 1)
            count1 = self.DFS_count(u, visited)

            '''2.b) Remove edge (u, v) and after removing the edge, count
                vertices reachable from u'''
            self.remove_edge(u, v)
            visited = [False] * (self.vertices + 1)
            count2 = self.DFS_count(u, visited)

            # 2.c) Add the edge back to the graph
            self.add_edge(u, v)

            # 2.d) If count1 is greater, then edge (u, v) is a bridge
            return False if count1 > count2 else True

    # Print Euler tour starting from vertex u
    def find_euler_cycle(self, u, edges) -> list:
        """
        :param u: starting vertex number
        :param edges: list passed between calls of function, on the first call is empty
        :return: list of edges
        """
        # Recur for all the vertices adjacent to this vertex
        for v in self.adjacency_dict[u]:
            # If edge u-v is not removed and it's a a valid next edge
            if self.is_next_edge_valid(u, v):
                edges.append([u, v])
                self.remove_edge(u, v)
                self.find_euler_cycle(v, edges)
        return edges

    def print_euler_cycle(self, u):
        """
        prints euler cycle
        :param u: starting vertex
        :return:
        """
        edges = []
        edges = self.find_euler_cycle(u, edges)
        for el in edges:
            print("{}-".format(el[0]), end='')
        print(edges[-1][1], end='')
        print()


def random_even_graphical_sequence(n) -> list:
    """
    returns random graphical sequence that is graphical and has even degrees
    :param n: number of vertices
    :return: graphical sequence as a list
    """
    graphical_sequence = []
    for i in range(n):
        rand_even_num = randrange(2, n, 2)
        graphical_sequence.append(rand_even_num)
    while not GraphReader().is_graphical_sequence(graphical_sequence):
        graphical_sequence = random_even_graphical_sequence(n)
    return graphical_sequence


def random_euler_graph(n) -> list:
    """
    generates random Euler graph
    :param n: number of vertices
    :return: adjacency list of a graph
    """
    randomizable_flag = False
    euler_graph = Graph()
    graphical_sequence = []
    while not randomizable_flag:
        graphical_sequence = random_even_graphical_sequence(n)
        result = GraphConverter.convert_graph(graphical_sequence, GraphRepresentation.GRAPHICAL_SEQUENCE,
                                              GraphRepresentation.ADJACENCY_LIST)
        euler_graph.set_graph((result, GraphRepresentation.ADJACENCY_LIST))
        randomizable_flag = euler_graph.randomize_graph_edges(17)
    print("Random graphical sequence: ", end='')
    print(*sorted(graphical_sequence))
    adj_list = convert_graph(euler_graph.adjacency_matrix, GraphRepresentation.ADJACENCY_MATRIX,
                             GraphRepresentation.ADJACENCY_LIST)
    return adj_list