import sys
import argparse

from Graph import Graph
from RandomGraphGenerator import *
from DictGraph import DictGraph, random_euler_graph
from GraphChecking import hamiltonian


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
        graph.visualise_graph_on_circle(bool(int(save_to_file)), file_name)
    else:
        print("Wrong input, try again")
        draw_graph()


def generate_graph() -> None:
    graph_type = input("Select type of the graph:\n"
                       "1 - G(n,l)\n"
                       "2 - G(n,p)\n"
                       "3 - K-regular\n"
                       "4 - Euler's graph and find Euler's cycle\n"
                       "Press any other key to return to the main menu\n"
                       )
    if graph_type in ["1", "2", "3", "4"]:
        n = input("Enter the number of graph vertices:\n")
        if graph_type == "1":
            l = input("Enter the number of graph edges:\n")
            try:
                graph.set_graph(random_graph_edges(int(n), int(l)))
            except Exception as e:
                print("Error: " + str(e) + "\nPlease try again\n")
                generate_graph()
        elif graph_type == "2":
            p = input("Enter the probability in range [0,1]:\n")
            try:
                graph.set_graph(random_graph_probability(int(n), float(p)))
            except Exception as e:
                print("Error: " + str(e) + "\nPlease try again\n")
                generate_graph()
        elif graph_type == "3":
            k = input("Enter the degree: \n")
            try:
                graph.set_graph(random_graph_regular(int(n), int(k)))
                print(graph.adjacency_matrix)
            except Exception as e:
                print("Error: " + str(e) + "\nPlease try again\n")
                generate_graph()
        elif graph_type == "4":
            try:
                generate_euler_graph(int(n))
            except ValueError as e:
                print("Error: " + str(e) + "\nPlease try again\n")
                generate_graph()
    else:
        main()


def read_graph() -> None:
    representation = input("Enter a representation of the input:\n"
                           "1 - Adjacency matrix\n"
                           "2 - Adjacency list\n"
                           "3 - Incidence matrix\n"
                           "4 - Graphical sequence\n"
                           "Press any other key to return to the main menu\n")
    if representation in ["1", "2", "3", "4"]:
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
                        '3 - incidence matrix \n,'
                        '4 - graphical sequence')

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
group.add_argument('--generate-k',
                   nargs=2,
                   metavar=('<nvertices>', '<degree>'),
                   type=int,
                   action='store',
                   help='Generate a k regular graph.')
group.add_argument('--generate-euler',
                   metavar=('<nvertices>'),
                   type=int,
                   action='store',
                   help='Generate Euler\'s graph. Number of vertices must be between 4-50')
parser.add_argument('--draw',
                    action='store',
                    metavar='<filename>',
                    nargs='?',
                    const=True,
                    help='Draw the graph. Specify filename if you want to save the image to the file')
parser.add_argument('--randomize',
                    action='store',
                    metavar='<nrandomizations>',
                    type=int,
                    nargs='?',
                    const=0,
                    help='Randomize the graph. Chose number of randomizations. Leave the argument '
                         'empty for a random number of randomizations from range [1-100]')
parser.add_argument('--find',
                    action='store_true',
                    help='Find connected components')
parser.add_argument('--check',
                    action='store',
                    metavar='<starting node>',
                    type=int,
                    help='Check if the graph is hamiltonian. Choose the node the path should start from (1 for the '
                         'default start)')
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
        if args.read[1] in ['1', '2', '3', '4']:
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
            graph.set_graph(random_graph_edges(n, p))
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    elif args.generate_k is not None:
        try:
            n = int(args.generate_k[0])
            k = int(args.generate_k[1])
            graph.set_graph(random_graph_regular(n, k))
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    elif args.generate_euler is not None:
        try:
            n = int(args.generate_euler)
            generate_euler_graph(n)
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            sys.exit(1)
    else:
        print("Data input option not specified. Please specify --read or --generate option\n")
        sys.exit(1)
    if args.find:
        find_connected_components()
    if args.check is not None:
        starting_node = args.check
        if not perform_check_hamiltonian(starting_node):
            sys.exit(1)
    if args.randomize is not None:
        number_of_randomizations = args.randomize
        if not perform_randomize_graph(number_of_randomizations):
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
                            "3 - Randomize graph edges\n"
                            "4 - Find connected components\n"
                            "5 - Check if the graph is hamiltonian\n"
                            "6 - Exit the program\n"
                            "Press any other key to return to the main menu\n")
                if job in ["1", "2", "3", "4", "5", "6"]:
                    if job == "1":
                        save_graph()
                    elif job == "2":
                        draw_graph()
                    elif job == "3":
                        randomize_graph()
                    elif job == "4":
                        find_connected_components()
                    elif job == "5":
                        check_hamiltonian()
                    elif job == "6":
                        sys.exit(1)
                else:
                    main()
        else:
            print("Wrong option selected, try again")
            main()


def randomize_graph():
    number_of_randomizations = input("Choose number of randomizations, zero for random in range "
                                     "1-100:\n")
    if not perform_randomize_graph(number_of_randomizations):
        randomize_graph()


def perform_randomize_graph(number_of_randomizations) -> bool:
    try:
        if not graph.randomize_graph_edges(int(number_of_randomizations)):
            print("An error occurred while randomizing graph edges")
        return True
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        return False


def find_connected_components():
    res = graph.find_components()
    print("Connected components of this graph")
    graph.print_components(res)


def generate_euler_graph(number_of_vertices):
    if number_of_vertices <= 3 or number_of_vertices > 50:
        raise ValueError("Number must be between 4-50")

    print(100 * '-')
    adj_list = random_euler_graph(number_of_vertices)
    graph.set_graph((adj_list, GraphRepresentation.ADJACENCY_LIST))
    dict_graph = DictGraph(adj_list)
    print("Found Euler's cycle:")
    dict_graph.print_euler_cycle(1)
    print(100 * '-')


def check_hamiltonian():
    starting_node = input("Choose the node the path should start from (1 for the default start)\n")
    if not perform_check_hamiltonian(starting_node):
        check_hamiltonian()


def perform_check_hamiltonian(starting_node) -> bool:
    try:
        result = hamiltonian(graph.adjacency_matrix, int(starting_node))
        if result[0]:
            print("The graph is hamiltonian. The path:\n")
            print(*result[1], sep=" -> ")
        else:
            print("The graph is not hamiltonian.")
        return True
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        return False


if __name__ == "__main__":
    graph = Graph()
    main()
