from random import random
from numpy.random import randint
from collections import defaultdict
import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import math


class FlowGraph:
    def __init__(self):
        self.flow_dict = {}
        self.layers = []

    def set_flow_dict(self, flow_dict):
        self.flow_dict = flow_dict

    def set_layers(self, layers):
        self.layers = layers


def add_edge(my_dict: dict, v1: int, v2: int) -> None:
    """ Add edge to flow graph"""
    capacity = random.randint(1, 10)
    my_dict[v1].append({'other_v': v2, 'capacity': capacity, 'flow': 0})


def generate_random_flow_graph(layers_num: int) -> (dict, list):
    """
    generates random flow graph with random edges and capacities and zero flow
    :param layers_num: number of layers between source and sink
    :return: dictionary of vertices and edges, list of vertices in layers
    """
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
    pairs = generate_possible_edges(vertices)

    my_dict = defaultdict(list)
    # basic connection between layers
    for i in range(layers_num + 1):
        out_num = vertices_in_layers[i]
        in_num = vertices_in_layers[i + 1]
        diff = out_num - in_num
        if diff == 0:
            vertices_shuffled = vertices[i+1][:]
            random.shuffle(vertices_shuffled)
            for c, el in enumerate(vertices_shuffled):
                add_edge(my_dict, vertices[i][c], el)
                pairs.remove((vertices[i][c], el))
                pairs.remove((el, vertices[i][c]))
        # more vertices in i layer than in i+1
        elif diff > 0:
            vertices_shuffled = vertices[i][:]
            random.shuffle(vertices_shuffled)
            for c in range(in_num):
                add_edge(my_dict, vertices_shuffled[c], vertices[i + 1][c])
                pairs.remove((vertices_shuffled[c], vertices[i + 1][c]))
                pairs.remove((vertices[i + 1][c], vertices_shuffled[c]))
            for c in range(in_num, out_num):
                random_sec = random.choice(vertices[i+1])
                add_edge(my_dict, vertices_shuffled[c], random_sec)
                pairs.remove((vertices_shuffled[c], random_sec))
                pairs.remove((random_sec, vertices_shuffled[c]))
        # more vertices in i+1 layer than in i
        elif diff < 0:
            vertices_shuffled = vertices[i+1][:]
            random.shuffle(vertices_shuffled)
            for c in range(out_num):
                add_edge(my_dict, vertices[i][c], vertices_shuffled[c])
                pairs.remove((vertices[i][c], vertices_shuffled[c]))
                pairs.remove((vertices_shuffled[c], vertices[i][c]))
            for c in range(out_num, in_num):
                random_sec = random.choice(vertices[i])
                add_edge(my_dict, random_sec, vertices_shuffled[c])
                pairs.remove((vertices_shuffled[c], random_sec))
                pairs.remove((random_sec, vertices_shuffled[c]))

    # adding random edges to the graph
    try:
        for i in range(2 * layers_num):
            el = random.choice(pairs)
            add_edge(my_dict, el[0], el[1])
            pairs.remove((el[0], el[1]))
            pairs.remove((el[1], el[0]))
    except IndexError:
        pass

    return my_dict, vertices


def prepare_multilayer_graph(graph_dict: dict, layers: list) -> nx.DiGraph:
    """
    prepare graph to drawing
    :param graph_dict: dictionary with edges - returned as first element from generate_random_flow_graph
    :param layers: list of vertices in layers - returned as first element from generate_random_flow_graph
    :return:
    """
    DG = nx.DiGraph()
    for c, layer in enumerate(layers):
        DG.add_nodes_from(layer, layer=c)
        for vertex in layer:
            vertex_data = graph_dict[vertex]
            for el in vertex_data:
                DG.add_edge(vertex, el['other_v'], weight=el['capacity'], flow=el["flow"])
    return DG


def draw_multilayer_graph(DG: nx.DiGraph, save_to_file: bool, file_name: str) -> None:
    """
    draws and optionaly saves to file graph
    :param DG: nx.Digraph from prepare_multilayer_graph
    :param save_to_file: if True saves to file
    :param file_name: name of file
    :return:
    """
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
    labels = nx.get_edge_attributes(DG, 'weight')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=labels, label_pos=0.3, rotate=False)

    if save_to_file:
        plt.rcParams['savefig.format'] = 'png'
        plt.savefig("data/" + file_name)
    plt.show()


def create_residual_graph(G):
    my_dict = defaultdict(list)
    for key in G:
        for el in G[key]:
            my_dict[key].append({'other_v': el['other_v'], 'c_f': el['capacity']})
            my_dict[el['other_v']].append({'other_v': key, 'c_f': 0})
    return my_dict


def generate_possible_edges(vertices):
    """
    generates possible edges between vertices
    :param vertices:
    :return:
    """
    vertices_without_st = vertices[1:-1]
    flattened_vertices = [i for el in vertices_without_st for i in el]
    res = []
    for idx, a in enumerate(flattened_vertices):
        for b in flattened_vertices[idx + 1:]:
            res.append((a, b))
            res.append((b, a))
    for el in vertices_without_st[0]:
        res.append(('s',el))
        res.append((el, 's'))
    for el in vertices_without_st[-1]:
        res.append((el,'t'))
        res.append(('t', el))
    return res


def draw_multilayer_graph_with_flow(DG, save_to_file, file_name):
    """
    draws and optionaly saves to file graph with flow and capacity
    :param DG:
    :param save_to_file:
    :param file_name:
    :return:
    """
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
    flows = nx.get_edge_attributes(DG, 'flow')
    capacities = nx.get_edge_attributes(DG, 'weight')
    labels = {}
    for key in capacities:
        labels[key] = str(flows[key])+'/'+str(capacities[key])
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=labels, label_pos=0.3, rotate=False)
    if save_to_file:
        plt.rcParams['savefig.format'] = 'png'
        plt.savefig("data/" + file_name)
    plt.show()


def BFS(G: dict):
    """
    finds path using breadth first search algorithm
    :param G:
    :return:
    """
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
    my_v = list(filter(lambda vertex: vertex['other_v'] == v2, d[v1]))
    if len(my_v) == 0:
        return False
    return True


def find_el(d, v1, v2):
    my_v = list(filter(lambda vertex: vertex['other_v'] == v2, d[v1]))
    return my_v[0]


def ford_fulkerson(G: dict):
    """
    find max flow in flow graph
    :param G: graph in which we want to find max flow
    :return: graph with best flows
    """
    Gf = create_residual_graph(G)

    while BFS(Gf) is not None:
        p = BFS(Gf)
        my_list = readableBFS(p)
        c_fs = []
        #finding c_f for augmenting path
        for i in range(len(my_list)-1):
            el = find_el(Gf, my_list[i], my_list[i+1])
            c_fs.append(el["c_f"])
        c_f = min(c_fs)

        #changing flow in augmenting path
        for i in range(len(my_list)-1):
            # change flow
            if is_edge_in_graph(G, my_list[i], my_list[i+1]):
                el_g = find_el(G, my_list[i], my_list[i+1])
                el_g['flow'] += c_f
            else:
                el_g = find_el(G, my_list[i+1], my_list[i])
                el_g['flow'] -= c_f
            # change residual edges
            el = find_el(Gf, my_list[i], my_list[i+1])
            el['c_f'] -= c_f
            reverse_el = find_el(Gf, my_list[i+1], my_list[i])
            reverse_el['c_f'] += c_f

    max_flow = 0
    for el in G['s']:
        max_flow += el['flow']
    print('Max_flow:{}'.format(max_flow))
    return G


if __name__=="__main__":
    list1 = [1,2,3]
    list2=list1[:]
    random.shuffle(list2)
    print(list1)
    print(list2)

