import sys
import argparse
import math
from Digraph import Digraph
from GraphConverter import GraphRepresentation


def save_digraph() -> None:
    filename_edges = input("Insert an output edges filename:\n")
    filename_weights = input("Insert an output weights filename:\n")
    if filename_weights != filename_edges:
        if digraph.save_to_file(filename_edges, filename_weights):
            print("Completed. Check folder data")
        else:
            print("An error occurred while saving the graph")
    else:
        print("Output file names must not be equal, try again")
        save_digraph()


def draw_digraph() -> None:
    try:
        file_name = input("Specify file name for the graph:\n")
        digraph.visualise_digraph(True, file_name)
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        draw_digraph()


def generate_digraph() -> None:
    n = int(input("Enter the number of graph vertices:\n"))
    p = float(input("Enter the value of probability:\n"))
    if not perform_generate(n, p):
        generate_digraph()


def perform_generate(n, p):
    try:
        digraph.random_digraph(n, p)
        return True
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        return False


def generate_strongly_connected_digraph():
    n = int(input("Enter the number of graph vertices:\n"))
    p = float(input("Enter the value of probability:\n"))
    try:
        digraph.strongly_connected_component(n, p)
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        generate_strongly_connected_digraph()


def read_digraph() -> None:
    filename_edges = input("Enter the name of the input file with digraph edges (stored in folder data):\n")
    filename_weights = input("Enter the name of the input file with digraph weights (stored in folder data):\n")
    if not perform_read(filename_edges, filename_weights):
        read_digraph()


def find_path(starting_point, target_point, arr):
    node = target_point
    paths_arr = []
    while node != starting_point:
        paths_arr.append(node)
        node = int(arr[node])
    paths_arr.append(starting_point)
    paths_arr.reverse()
    return paths_arr


def perform_shortest_paths(s):
    try:
        result = digraph.shortest_paths_bellman(s)
        if result:
            print("\nDistances from " + str(result[2]) + " node:")
            for i, item in enumerate(result[0]):
                paths = ""
                if i != s:
                    path = find_path(result[2], i, result[1])
                    for j, node in enumerate(path):
                        if j < len(path)-1:
                            paths = paths + str(node) + " -> "
                        else:
                            paths = paths + str(node)
                print(str(i) + " : " + str(int(item)) + ", path: " + paths)
            return True
        else:
            print("Negative values cycle detected. Try again with different node")
            return False
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        return False


def shortest_paths():
    s = input("Enter the starting node (max value = " + str(digraph.vertices-1) + "):\n")

    if not perform_shortest_paths(int(s)):
        shortest_paths()


def perform_johnson(fixing=False):
    try:
        result = digraph.johnson(fixing)
        if result[0]:
            print("\nDistances matrix:")
            format_row = "{:>5}" * len(result[1])
            for row in result[1]:
                print(format_row.format(*row))
        else:
            print("Negative values cycle detected. Weights will be changed so that no negative cycles exists.")
            perform_johnson(fixing=True)
        return True
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        return False


def shortest_paths_johnson(fixing=False):
    if not perform_johnson(fixing):
        main()


parser = argparse.ArgumentParser(description='Command line interface for graph app.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--read',
                   action='store',
                   nargs=2,
                   metavar=('<edges filename>', '<weights filename>'),
                   help='Read input from a files.'
                        'File has to be stored in folder data. Digraph must be coded as adjacency matrix:\n')
group.add_argument('--generate-np',
                   nargs=2,
                   metavar=('<nvertices>', '<probability>'),
                   action='store',
                   help='Generate an np graph.')
group.add_argument('--generate-connected-np',
                   nargs=2,
                   metavar=('<nvertices>', '<probability>'),
                   action='store',
                   help='Generate a strongly connected np graph.')
parser.add_argument('--shortest-paths-bellman',
                   metavar='<starting_node>',
                   type=int,
                   action='store',
                   help='Find shortest paths in biggest connected component using Bellman-Ford algorithm.')
parser.add_argument('--shortest-paths-johnson',
                   action='store_true',
                   help='Find shortest paths using Johnson\' algorithm.')
parser.add_argument('--connected-components',
                   action='store_true',
                   help='Find connected components using Kosaraju\'s algorithm.')
parser.add_argument('--draw',
                    action='store',
                    metavar='<filename>',
                    help='Draw the graph. Specify file name for the graph image')
parser.add_argument('--save',
                    action='store',
                    nargs=2,
                    metavar=('<filename_edges>', '<filename_weights>'),
                    help='Save graph to the files (separate file for graph edges and edge weights).')


def perform_read(filename_edges, filename_weights):
    try:
        digraph.read_data(filename_edges, filename_weights)
        return True
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        return False


def run_cmd_app(args):
    if args.read is not None:
        filename_edges = args.read[0]
        filename_weights = args.read[1]
        if not perform_read(filename_edges, filename_weights):
            sys.exit(1)
    elif args.generate_np is not None:
        try:
            n = int(args.generate_np[0])
            p = float(args.generate_np[1])
            perform_generate(n, p)
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    elif args.generate_connected_np is not None:
        try:
            n = int(args.generate_connected_np[0])
            p = float(args.generate_connected_np[1])
            digraph.strongly_connected_component(n, p)
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    else:
        print("Data input option not specified. Please specify --read or --generate option\n")
        sys.exit(1)
    if args.connected_components:
        connected_components()
    if args.shortest_paths_bellman is not None:
        try:
            starting_node = args.shortest_paths_bellman
            perform_shortest_paths(starting_node)
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    if args.draw is not None:
        file_name = args.draw
        try:
            digraph.visualise_digraph(True, file_name)
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    if args.shortest_paths_johnson:
        if not perform_johnson():
            sys.exit(1)
    if args.save is not None:
        filename_edges = args.save[0]
        filename_weights = args.save[1]
        if filename_edges != filename_weights:
            if not digraph.save_to_file(filename_edges, filename_weights):
                sys.exit(1)
        else:
            print('Output file names must not be equal, try again')
            sys.exit(1)


def connected_components():
    comp, nr = digraph.kosaraju()
    print("The graph has: " + str(nr) + " connected components:")
    for i in range(1, nr+1):
        items = []
        for j, item in enumerate(comp):
            if item == i:
                items.append(j)
        itemsstr = ""
        for item in items:
            itemsstr += str(item)
            itemsstr += ", "
        print(str(i) + " -> " + itemsstr)


def shortest_paths_bellman():
    s = input("Enter the starting node (max value = " + str(digraph.vertices - 1) + "):\n")
    try:
        result = digraph.shortest_paths_bellman(int(s))
        if result:
            print("\nDistances from " + str(result[2]) + " node:")
            for i, item in enumerate(result[0]):
                paths = ""
                if i != s:
                    path = find_path(result[2], i, result[1])
                    for j, node in enumerate(path):
                        if j < len(path)-1:
                            paths = paths + str(node) + " -> "
                        else:
                            paths = paths + str(node)
        else:
            print("Negative values cycle detected. Try again with different node")
            shortest_paths()
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        shortest_paths()


def main() -> None:
    if len(sys.argv) > 1:
        args = parser.parse_args()
        run_cmd_app(args)
    else:
        job = input("Select an option:\n"
                    "1 - Read the digraph from file \n"
                    "2 - Generate a random G(n,p) digraph \n"
                    "3 - Generate a random strongly conected digraph \n"
                    )

        if job in ["1", "2", "3"]:
            if job == "1":
                read_digraph()
            if job == "2":
                generate_digraph()
            if job == "3":
                generate_strongly_connected_digraph()
            while True:
                job = input("Choose what you want to do with the graph:\n"
                            "1 - Find connected components using Kosaraju\'s algorithm\n"
                            "2 - Find shortest path from starting vertex using the Bellman\'s-Ford algorithm\n"
                            "3 - Find shortest paths using the Johnson algorithm\n"
                            "4 - Save the graph to the file\n"
                            "5 - Draw the graph\n"
                            "6 - Exit the program\n"
                            "Press any other key to return to the main menu\n")
                if job in ["1", "2", "3", "4", "5", "6"]:
                    if job == "1":
                        connected_components()
                    if job == "2":
                        shortest_paths_bellman()
                    if job == "3":
                        shortest_paths_johnson()
                    if job == "4":
                        save_digraph()
                    if job == "5":
                        draw_digraph()
                    if job == "6":
                        sys.exit(1)
                else:
                    main()
        else:
            print("Wrong option selected, try again")
            main()


if __name__ == "__main__":
    digraph = Digraph()
    main()
