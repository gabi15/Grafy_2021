import sys
import argparse
from copy import deepcopy

from Graph import Graph
from RandomWeightedGraphGenerator import *
from MinimumSpanningTree import *


def save_graph() -> None:
    representation = input("Select an output representation:\n"
                           "2 - Adjacency list\n"
                           "3 - Incidence matrix\n"
                           )
    if representation in ["1", "2", "3"]:
        filename = input("Insert an output filename:\n")
        perform_save(int(representation), filename)
    else:
        print("Wrong representation selected, try again")
        save_graph()


def perform_save(representation, filename) -> bool:
    if graph.save_to_file(GraphRepresentation(representation), filename):
        print("Saving completed. Check folder data")
        return True
    else:
        print("An error occurred while saving the graph")
        return False


def draw_graph() -> None:
    save_to_file = input("Do you want to save image to a file? Select an option:\n"
                         "0 - No\n"
                         "1 - Yes\n"
                         )
    if save_to_file in ["0", "1"]:
        file_name = ""
        if save_to_file == "1":
            try:
                file_name = input("Specify file name for the graph:\n")
            except Exception as e:
                print("Error: " + str(e) + "\nPlease try again\n")
        graph.visualize_graph_with_weights(bool(int(save_to_file)), file_name)
    else:
        print("Wrong input, try again")
        draw_graph()


def generate_graph() -> None:
    print("Select number of vertices and probability for the G(n,p) weighted graph:")
    n = input("Enter the number of graph vertices:\n")
    p = input("Enter the probability in range [0,1]:\n")
    try:
        graph.set_graph(random_weighted_graph_probability(int(n), float(p)))
        while max(graph.find_components()) > 1:
            graph.set_graph(random_weighted_graph_probability(int(n), float(p)))
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        generate_graph()


parser = argparse.ArgumentParser(description='Command line interface for graph app.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--read',
                   action='store',
                   metavar='<filename>',
                   help='Read input from a file.'
                        'Enter the name of the input file (stored in folder data) with the adjacency matrix.\n')
group.add_argument('--generate-np',
                    nargs=2,
                    metavar=('<nvertices>', '<probability>'),
                    action='store',
                    help='Generate an np graph.')
parser.add_argument('--shortest-paths',
                    metavar='<starting_node>',
                    type=int,
                    action='store',
                    help='Find shortest paths using Dijkstra algorithm.')
parser.add_argument('--distances-matrix',
                    action='store_true',
                    help='Find distances matrix.')
parser.add_argument('--center',
                    action='store_true',
                    help='Find center of the graph.')
parser.add_argument('--center-minimax',
                    action='store_true',
                    help='Find minimax center of the graph.')
parser.add_argument('--minimal-spanning-tree',
                    action='store_true',
                    help='Find minimal spanning tree of the graph.')
parser.add_argument('--draw',
                    action='store',
                    metavar='<filename>',
                    nargs='?',
                    const=True,
                    help='Draw the graph. Specify filename if you want to save the image to the file')
parser.add_argument('--save',
                    action='store',
                    nargs=2,
                    metavar=('<filename>', '<representation>'),
                    help='Save graph to the file with given name and representation.'
                         'Available output representations:\n'
                         '1 - adjacency matrix,\n '
                         '2 - adjacency list, \n'
                         '3 - incidence matrix \n')


def run_cmd_app(args):
    if args.read is not None:
        if not perform_read(1, args.read):
            sys.exit(1)
    elif args.generate_np is not None:
        try:
            n = int(args.generate_np[0])
            p = float(args.generate_np[1])
            graph.set_graph(random_weighted_graph_probability(n, p))
            while max(graph.find_components()) > 1:
                graph.set_graph(random_weighted_graph_probability(n, p))
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    else:
        print("Data input option not specified. Please specify --read or --generate option\n")
        sys.exit(1)
    if args.save is not None:
        if args.save[1] in ["1", "2", "3"]:
            representation = int(args.save[1])
            filename = args.save[0]
            if not perform_save(representation, filename):
                sys.exit(1)
    if args.shortest_paths is not None:
        try:
            starting_node = args.shortest_paths
            print("Shortest paths starting at node: " + str(args.shortest_paths) + " \n")
            graph.print_dijkstra(starting_node)
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    if args.draw is not None:
        if args.draw is not True:
            file_name = args.draw
            try:
                graph.visualize_graph_with_weights(True, file_name)
            except Exception as e:
                print("Error: " + str(e) + "\nPlease try again\n")
                sys.exit(1)
        else:
            graph.visualize_graph_with_weights(False, None)
    if args.distances_matrix:
        print("Distances matrix of generated graph:")
        find_distances_matrix()
    if args.center:
        print("Center of generated graph:")
        find_center()
    if args.center_minimax:
        print("Center minimax of generated graph:")
        find_minimax_center()
    if args.minimal_spanning_tree:
        print("Minimal spanning tree of generated graph:")
        find_minimal_spanning_tree()


def read_graph() -> None:
    filename = input("Enter the name of the input file (stored in folder data) with the adjacency matrix:\n")
    if not perform_read(1, filename):
        read_graph()


def perform_read(representation: int, filename: str) -> bool:
    try:
        graph.read_data(GraphRepresentation(representation), filename)
        return True
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        return False


def find_shortest_paths():
    try:
        starting_node = input("Enter node to start with:\n")
        graph.print_dijkstra(int(starting_node))
    except Exception:
        print("Wrong input, try again\n")
        find_shortest_paths()


def find_distances_matrix():
    res = graph.find_distances_matrix()
    format_row = "{:>8}" * len(res)
    for row in res:
        print(format_row.format(*row))


def find_center():
    centers, centers_sum = graph.find_center()
    print(f'Center nodes: {centers}')
    print(f'Sum: {int(centers_sum)}')


def find_minimax_center():
    minimax_centers, minimax_centers_max = graph.find_minimax_center()
    print(f'Center nodes: {minimax_centers}')
    print(f'Minimax: {int(minimax_centers_max)}')


def find_minimal_spanning_tree():
    graph_copy = deepcopy(graph)
    graph_copy.set_graph(minimum_spanning_tree(graph_copy.adjacency_matrix))
    graph_copy.visualize_graph_with_weights(False, "")
    del graph_copy


def main() -> None:
    if len(sys.argv) > 1:
        args = parser.parse_args()
        run_cmd_app(args)
    else:
        job = input("Select an option:\n"
                    "1 - Read the graph from file \n"
                    "2 - Generate a random graph \n"
                    )

        if job in ["1", "2"]:
            if job == "1":
                read_graph()
            if job == "2":
                generate_graph()
            while True:
                job = input("Choose what you want to do with the graph:\n"
                            "1 - Save the graph to the file\n"
                            "2 - Draw the graph\n"
                            "3 - Find shortest paths\n"
                            "4 - Find distances matrix\n"
                            "5 - Find center\n"
                            "6 - Find minimax center\n"
                            "7 - Find minimal spanning tree\n"
                            "8 - Exit the program\n"
                            "Press any other key to return to the main menu\n")
                if job in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                    if job == "1":
                        save_graph()
                    elif job == "2":
                        draw_graph()
                    elif job == "3":
                        find_shortest_paths()
                    elif job == "4":
                        find_distances_matrix()
                    elif job == "5":
                        find_center()
                    elif job == "6":
                        find_minimax_center()
                    elif job == "7":
                        find_minimal_spanning_tree()
                    elif job == "8":
                        sys.exit(1)
                else:
                    main()
        else:
            print("Wrong option selected, try again")
            main()


if __name__ == "__main__":
    graph = Graph()
    main()
