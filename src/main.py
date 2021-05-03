import sys

from Graph import Graph
from RandomGraphGenerator import *


def save_graph() -> None:
    representation = input("Select an output representation:\n"
                               "1 - Adjacency matrix\n"
                               "2 - Adjacency list\n"
                               "3 - Incidence matrix\n"
                               )
    if representation in ["1", "2", "3"]:
        filename = input("Insert an output filename:\n")
        if graph.save_to_file(GraphRepresentation(int(representation)), filename):
            print("Completed. Check folder data")
        else:
            print("An error occurred while saving the graph")
    else:
        print("Wrong representation selected, try again")
        save_graph()


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
                           "Press any other key to return to the main menu\n"
                           )
    if graph_type in ["1", "2"]:
        n = input("Enter the number of graph vertices:\n")
        if graph_type == "1":
            l = input("Enter the number of graph edges:\n")
            try:
                graph.set_graph(random_graph_edges(int(n), int(l)))
            except Exception as e:
                print("Error: " + str(e) + "\nPlease try again\n")
                generate_graph()
        if graph_type == "2":
            p = input("Enter the probability in range [0,1]:\n")
            try:
                graph.set_graph(random_graph_probability(int(n), float(p)))
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
                           "4 - Graphical sequence\n"
                           "Press any other key to return to the main menu\n")
    if representation in ["1", "2", "3", "4"]:
        filename = input("Enter the name of the input file (stored in folder data):\n")
        try:
            graph.read_data(GraphRepresentation(int(representation)), filename)
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            read_graph()
    else:
        main()


def main() -> None:
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
                            "5 - Exit the program\n"
                            "Press any other key to return to the main menu\n")
            if job in ["1", "2", "3", "4", "5"]:
                if job == "1":
                    save_graph()
                if job == "2":
                    draw_graph()
                if job == "3":
                    number_of_randomizations = int(
                        input("Choose number of randomizations, zero for random in range 1-100:\n"))

                    if not randomize_graph(number_of_randomizations):
                        print("Graph cannot be randomized.")
                if job == "4":
                    find_connected_components()
                if job == "5":
                    sys.exit(1)
            else:
                main()
    else:
        print("Wrong option selected, try again")
        main()


def randomize_graph(number_of_randomizations):
    return graph.randomize_graph_edges(number_of_randomizations)


def find_connected_components():
    res = graph.find_components()
    print("Connected components of this graph")
    graph.print_components(res)


if __name__ == "__main__":
    graph = Graph()
    main()
