from random import randrange, random
from numpy.random import randint
from collections import defaultdict
import numpy as np
import random
import itertools
import matplotlib.pyplot as plt
import networkx as nx

from networkx.utils import pairwise


def add_edge(my_dict, v1, v2):
    capacity = random.randint(1, 10)
    my_dict[v1].append({'other_v': v2, 'capacity': capacity, 'flow': 0})


def random_flow(layers_num):
    # random number of vertices in layers
    vertices_in_layers = randint(2, high=layers_num+1, size=layers_num)
    vertices_in_layers = np.insert(vertices_in_layers, 0, 1)
    vertices_in_layers = np.append(vertices_in_layers, 1)
    counter = 0
    vertices = []

    # indexed vertices in layers
    for el in vertices_in_layers:
        vertices.append(list(range(counter, counter+el)))
        counter += el
    vertices[0][0] = 's'
    vertices[layers_num+1][0] = 't'

    # every possible edge
    pairs = []
    for i in range(layers_num+1):
        for el1 in vertices[i]:
            for el2 in vertices[i+1]:
                pairs.append((el1, el2))
                pairs.append((el2, el1))

    my_dict = defaultdict(list)
    # basic connection between layers
    for i in range(layers_num+1):
        out_num = vertices_in_layers[i]
        in_num = vertices_in_layers[i+1]
        diff = out_num-in_num
        if diff == 0:
            for c in range(out_num):
                add_edge(my_dict, vertices[i][c], vertices[i+1][c])
                pairs.remove((vertices[i][c], vertices[i+1][c]))
                pairs.remove((vertices[i+1][c], vertices[i][c]))
        elif diff > 0:
            s_c = 0
            for c in range(out_num):
                add_edge(my_dict, vertices[i][c], vertices[i + 1][s_c])
                pairs.remove((vertices[i][c], vertices[i+1][s_c]))
                pairs.remove((vertices[i+1][s_c], vertices[i][c]))
                s_c += 1
                if s_c >= in_num:
                    s_c = 0
        elif diff < 0:
            f_c = 0
            for c in range(in_num):
                add_edge(my_dict, vertices[i][f_c], vertices[i + 1][c])
                pairs.remove((vertices[i][f_c], vertices[i + 1][c]))
                pairs.remove((vertices[i+1][c], vertices[i][f_c]))
                f_c += 1
                if f_c >= out_num:
                    f_c = 0
    # adding random edges to the graph
    try:
        for i in range(2*layers_num):
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
    #plt.axis("equal")
    labels = nx.get_edge_attributes(DG, 'weight')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=labels, label_pos=0.3, rotate=False)
    plt.show()


if __name__ == "__main__":
    multi_dict = random_flow(4)
    graph = prepare_multilayer_graph(multi_dict[0], multi_dict[1])
    draw_multilayer_graph(graph)













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


    #G = multilayered_graph(*subset_sizes)


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




