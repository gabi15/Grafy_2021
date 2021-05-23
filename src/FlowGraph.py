from random import randrange, random
from numpy.random import randint
from collections import defaultdict
import numpy as np
import random
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import math
import copy

from networkx.utils import pairwise


def add_edge(my_dict, v1, v2):
    capacity = random.randint(1, 10)
    my_dict[v1].append({'other_v': v2, 'capacity': capacity, 'flow': 0})


def random_flow(layers_num):
    # random number of vertices in layers
    vertices_in_layers = randint(2, high=layers_num + 1, size=layers_num)
    vertices_in_layers = np.insert(vertices_in_layers, 0, 1)
    vertices_in_layers = np.append(vertices_in_layers, 1)
    counter = 0
    vertices = []

    # indexed vertices in layers
    for el in vertices_in_layers:
        vertices.append(list(range(counter, counter + el)))
        counter += el
    vertices[0][0] = 's'
    vertices[layers_num + 1][0] = 't'

    # every possible edge
    pairs = []
    for i in range(layers_num + 1):
        for el1 in vertices[i]:
            for el2 in vertices[i + 1]:
                pairs.append((el1, el2))
                pairs.append((el2, el1))

    my_dict = defaultdict(list)
    # basic connection between layers
    for i in range(layers_num + 1):
        out_num = vertices_in_layers[i]
        in_num = vertices_in_layers[i + 1]
        diff = out_num - in_num
        if diff == 0:
            for c in range(out_num):
                add_edge(my_dict, vertices[i][c], vertices[i + 1][c])
                pairs.remove((vertices[i][c], vertices[i + 1][c]))
                pairs.remove((vertices[i + 1][c], vertices[i][c]))
        elif diff > 0:
            s_c = 0
            for c in range(out_num):
                add_edge(my_dict, vertices[i][c], vertices[i + 1][s_c])
                pairs.remove((vertices[i][c], vertices[i + 1][s_c]))
                pairs.remove((vertices[i + 1][s_c], vertices[i][c]))
                s_c += 1
                if s_c >= in_num:
                    s_c = 0
        elif diff < 0:
            f_c = 0
            for c in range(in_num):
                add_edge(my_dict, vertices[i][f_c], vertices[i + 1][c])
                pairs.remove((vertices[i][f_c], vertices[i + 1][c]))
                pairs.remove((vertices[i + 1][c], vertices[i][f_c]))
                f_c += 1
                if f_c >= out_num:
                    f_c = 0
    # adding random edges to the graph
    try:
        for i in range(2 * layers_num):
            el = random.choice(pairs)
            add_edge(my_dict, el[0], el[1])
            pairs.remove((el[0], el[1]))
            pairs.remove((el[1], el[0]))
    except IndexError:
        print('aaa')

    return my_dict, vertices


def prepare_multilayer_graph(graph_dict, layers):
    DG = nx.DiGraph()
    for c, layer in enumerate(layers):
        DG.add_nodes_from(layer, layer=c)
        for vertex in layer:
            vertex_data = graph_dict[vertex]
            for el in vertex_data:
                DG.add_edge(vertex, el['other_v'], weight=el['capacity'])
    return DG


def draw_multilayer_graph(DG):
    subset_color = [
        "gold",
        "violet",
        "limegreen",
        "darkorange",
        "violet",
        "green",
        "blue"
    ]

    color = [subset_color[data["layer"]] for v, data in DG.nodes(data=True)]
    pos = nx.multipartite_layout(DG, subset_key="layer")
    plt.figure(figsize=(8, 8))
    nx.draw(DG, pos, node_color=color, with_labels=True)
    # plt.axis("equal")
    labels = nx.get_edge_attributes(DG, 'weight')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=labels, label_pos=0.3, rotate=False)
    plt.show()


def create_residual_graph(G):
    my_dict = defaultdict(list)
    for key in G:
        for el in G[key]:
            my_dict[key].append({'other_v': el['other_v'], 'c_f': el['capacity'], 'flow': 0})
            my_dict[el['other_v']].append({'other_v': key, 'c_f': 0, 'flow': 0})
    return my_dict


def BFS(G):
    d = {}
    p = {}
    for key in G:
        d[key] = math.inf
        p[key] = None
    d['s'] = 0
    queue = {'s': G['s']}
    while len(queue) != 0:
        first_key = list(queue)[0]
        v = queue.pop(first_key)
        for neighbour in v:
            if math.isinf(d[neighbour['other_v']]) and neighbour['c_f'] != 0:
                d[neighbour['other_v']] = d[first_key]+1
                p[neighbour['other_v']] = first_key
                queue[neighbour['other_v']] = G[neighbour['other_v']]
                if neighbour['other_v'] == 't':
                    return p
    return None


def readableBFS(p):
    vertex = 't'
    vertices = []
    while vertex is not None:
        vertices.append(vertex)
        vertex = p[vertex]
    vertices.reverse()
    return vertices


def is_edge_in_graph(d, v1, v2):
    # neigbours = G[v1]
    # for c,el in enumerate(neigbours):
    #     if el['other_v'] == v2:
    #         return True, c
    # return False
    my_v = list(filter(lambda vertex: vertex['other_v'] == v2, d[v1]))
    if len(my_v) == 0:
        return False
    return True


def find_el(d, v1, v2):
    my_v = list(filter(lambda vertex: vertex['other_v'] == v2, d[v1]))
    return my_v[0]


def ford_fulkerson(G):
    Gf = create_residual_graph(G)

    while BFS(Gf) is not None:
        p = BFS(G)
        my_list = readableBFS(p)
        c_fs = []
        #finding c_f for augmenting path
        for i in range(len(my_list)-2):
            el = find_el(my_list[i], my_list[i+1])
            c_fs.append(el["c_f"])
        c_f = min(c_fs)

        #changing flow in augmenting path
        for i in range(len(my_list)-2):
            el = find_el(Gf, my_list[i], my_list[i+1])
            if is_edge_in_graph(G, my_list[i], my_list[i+1]):
                el['flow'] += c_f
                el['c_f'] -= c_f
            else:
                el['flow'] -= c_f
                el['c_f'] = el['flow']




if __name__ == "__main__":
    multi_dict = random_flow(2)
    # graph = prepare_multilayer_graph(multi_dict[0], multi_dict[1])
    # draw_multilayer_graph(graph)
    # print(multi_dict[0])
    # gf = create_residual_graph(multi_dict[0])
    # print(gf)
    # p = BFS(gf)
    # print(p)
    # print(readableBFS(p))


    print(multi_dict[0])


    # el[1]['c']=5
    # print(hh)

    # DG = nx.DiGraph()
    # DG.add_nodes_from([1, 2, 3])
    # DG.add_edge((2, 3, {'weight': 3}))
    # G = nx.complete_multipartite_graph(2, 16, 10)
    # pos = nx.multipartite_layout(G)
    # layout = nx.spring_layout(G)
    # labels = nx.get_edge_attributes(G, "weight")
    # nx.draw(G, layout, with_labels=True)
    # nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    # plt.show()

    # subset_sizes = [5, 5, 4, 3, 2, 4, 4, 3]
    # subset_color = [
    #     "gold",
    #     "violet",
    #     "limegreen",
    #     "darkorange",
    #     "violet"
    # ]
    #
    #
    # def multilayered_graph(*subset_sizes):
    #     extents = pairwise(itertools.accumulate((0,) + subset_sizes))
    #     print(extents)
    #     layers = [range(start, end) for start, end in extents]
    #     print(layers)
    #     G = nx.Graph()
    #     for (i, layer) in enumerate(layers):
    #         G.add_nodes_from(layer, layer=i)
    #     for layer1, layer2 in pairwise(layers):
    #         G.add_edges_from(itertools.product(layer1, layer2))
    #     return G

    # G = multilayered_graph(*subset_sizes)

    # G = nx.DiGraph()
    # G.add_nodes_from(['s'], layer=1)
    # G.add_nodes_from([2,3],layer=2)
    # G.add_nodes_from([4, 5], layer=3)
    # G.add_nodes_from([6], layer=4)
    # G.add_edges_from([('s', 2), ('s', 3),(2, 4),(3,5),(4,6),(5,6)],weight=3)
    # G.add_edge(3,'s',weight=2)
    #
    # color = [subset_color[data["layer"]] for v, data in G.nodes(data=True)]
    # pos = nx.multipartite_layout(G, subset_key="layer")
    # plt.figure(figsize=(8, 8))
    # nx.draw(G, pos, node_color=color, with_labels=True)
    # plt.axis("equal")
    # labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    # plt.show()
