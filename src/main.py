import sys
import argparse

from Graph import Graph
from RandomGraphGenerator import *
from RandomWeightedGraphGenerator import *


def save_graph() -> None:
    representation = input("Select an output representation:\n"
                               "1 - Adjacency matrix\n"
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
        print("Completed. Check folder data")
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
    graph_type = input("Select type of the weighted graph:\n"
                       "1 - G(n,l)\n"
                       "2 - G(n,p)\n"
                       "Press any other key to return to the main menu\n"
                       )
    if graph_type in ["1", "2"]:
        n = input("Enter the number of graph vertices:\n")
        if graph_type == "1":
            l = input("Enter the number of graph edges:\n")
            try:
                graph.set_graph(random_weighted_graph_edges(int(n), int(l)))
            except Exception as e:
                print("Error: " + str(e) + "\nPlease try again\n")
                generate_graph()
        elif graph_type == "2":
            p = input("Enter the probability in range [0,1]:\n")
            try:
                graph.set_graph(random_weighted_graph_probability(int(n), float(p)))
            except Exception as e:
                print("Error: " + str(e) + "\nPlease try again\n")
                generate_graph()
    else:
        main()


def read_graph() -> None:
    representation = input("Enter a representation of the input:\n"
                           "1 - Adjacency matrix\n"
                           "2 - Adjacency list\n"
                           "3 - Incidence matrix\n"
                           "Press any other key to return to the main menu\n"
                           )
    if representation in ["1", "2", "3"]:
        filename = input("Enter the name of the input file (stored in folder data):\n")
        if not perform_read(int(representation), filename):
            read_graph()
    else:
        main()


def perform_read(representation: int, filename: str) -> bool:
    try:
        graph.read_data(GraphRepresentation(representation), filename)
        return True
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        return False


parser = argparse.ArgumentParser(description='Command line interface for graph app.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--read',
                   action='store',
                   nargs=2,
                   metavar=('<filename>', '<representation>'),
                   help='Read input from a file with given name and representation.'
                        'File has to be stored in folder data. Available input representations:\n'
                        '1 - adjacency matrix,\n '
                        '2 - adjacency list, \n'
                        '3 - incidence matrix')

group.add_argument('--generate-nl',
                   nargs=2,
                   metavar=('<nvertices>', '<nedges>'),
                   type=int,
                   action='store',
                   help='Generate an nl graph.')
group.add_argument('--generate-np',
                   nargs=2,
                   metavar=('<nvertices>', '<probability>'),
                   action='store',
                   help='Generate an np graph.')
group.add_argument('--print_dijkstra',
                   nargs=1,
                   metavar='<starting_node>',
                   action='store',
                   help='Perform Dijkstra algorithm.')
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
    print(args)
    if args.read is not None:
        if args.read[1] in ['1', '2', '3']:
            representation = int(args.read[1])
            filename = args.read[0]
            if not perform_read(representation, filename):
                sys.exit(1)
    elif args.generate_nl is not None:
        try:
            n = int(args.generate_nl[0])
            l = int(args.generate_nl[1])
            graph.set_graph(random_graph_edges(n, l))
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    elif args.generate_np is not None:
        try:
            n = int(args.generate_np[0])
            p = float(args.generate_np[1])
            graph.set_graph(random_graph_probability(n, p))
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    else:
        print("Data input option not specified. Please specify --read or --generate option\n")
        sys.exit(1)
    if args.draw is not None:
        if args.draw is not True:
            file_name = args.draw
            try:
                graph.visualise_graph_on_circle(True, file_name)
            except Exception as e:
                print("Error: " + str(e) + "\nPlease try again\n")
                sys.exit(1)
        else:
            graph.visualise_graph_on_circle(False, None)
    if args.save is not None:
        if args.save[1] in ["1", "2", "3"]:
            representation = int(args.save[1])
            filename = args.save[0]
            if not perform_save(representation, filename):
                sys.exit(1)
    if args.print_dijkstra is not None:
        starting_node = args.print_dijkstra
        try:
            graph.print_dijkstra(starting_node)
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)


def find_shortest_paths():
    try:
        starting_node = input("Enter node to start with:\n")
        graph.print_dijkstra(int(starting_node))
    except Exception as e:
        print("Wrong input, try again\n")
        find_shortest_paths()


def find_distances_matrix():
    pass


def find_center():
    pass


def find_minimax_center():
    pass


def find_minimal_spanning_tree():
    pass


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
                            "6 - Find minimax center"
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
