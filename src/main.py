import sys

from Digraph import Digraph
from GraphRepresentation import GraphRepresentation


def save_digraph() -> None:
    representation = input("Select an output representation:\n"
                           "1 - Adjacency matrix\n"
                           "2 - Adjacency list\n"
                           "3 - Incidence matrix\n"
                           )
    if representation in ["1", "2", "3"]:
        filename = input("Insert an output filename:\n")
        if digraph.save_to_file(GraphRepresentation(int(representation)), filename):
            print("Completed. Check folder data")
        else:
            print("An error occurred while saving the graph")
    else:
        print("Wrong representation selected, try again")
        save_digraph()


def draw_digraph() -> None:
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
        digraph.visualise_digraph(True, bool(int(save_to_file)), file_name)
    else:
        print("Wrong input, try again")
        draw_digraph()


def generate_digraph() -> None:
    n = input("Enter the number of graph vertices:\n")
    p = input("Enter the value of probability:\n")
    try:
        digraph.random_digraph(int(n), float(p))
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        generate_digraph()


def generate_strongly_connected_digraph():
    generate_digraph()
    digraph.strongly_connected_component()
    print("Generated strongly connected graph has " + str(digraph.vertices) + " vertices\n")


def read_digraph() -> None:
    representation = input("Enter a representation of the input:\n"
                           "1 - Adjacency matrix\n"
                           "2 - Adjacency list\n"
                           "3 - Incidence matrix\n"
                           "Press any other key to return to the main menu\n"
                           )
    if representation in ["1", "2", "3"]:
        filename = input("Enter the name of the input file (stored in folder data):\n")
        try:
            digraph.read_data(GraphRepresentation(int(representation)), filename)
        except Exception as e:
            print("Error: " + str(e) + "\nPlease try again\n")
            read_digraph()
    else:
        main()


def shortest_paths():
    s = input("Enter the starting node (max value = " + str(digraph.vertices) + "):\n")
    try:
        result = digraph.bellman_ford(int(s))
        if result:
            print("Distances from " + str(s) + " node:\n")
            for i, item in enumerate(result[0]):
                print(str(i) + " -> " + str(item))
        else:
            print("Negative values cycle detected. Try again with different node")
            shortest_paths()
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        shortest_paths()


def shortest_paths_johnson(fixing=False):
    try:
        result = digraph.johnson(fixing)
        if result[0]:
            print(result[1])
        else:
            print("Negative values cycle detected. Weights will be changed so that no negative cycles exists.")
            shortest_paths_johnson(fixing=True)
    except Exception as e:
        print("Error: " + str(e) + "\nPlease try again\n")
        main()


def main() -> None:
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
                        "1 - Find shortest path from starting vertex\n"
                        "2 - Find shortest paths using the Johnson algorithm\n"
                        "3 - Save the graph to the file\n"
                        "4 - Draw the graph\n"
                        "5 - Exit the program\n"
                        "Press any other key to return to the main menu\n")
            if job in ["1", "2", "3", "4", "5"]:
                if job == "1":
                    shortest_paths()
                if job == "2":
                    shortest_paths_johnson()
                if job == "3":
                    save_digraph()
                if job == "4":
                    draw_digraph()
                if job == "5":
                    sys.exit(1)
            else:
                main()
    else:
        print("Wrong option selected, try again")
        main()


if __name__ == "__main__":
    digraph = Digraph()
    main()
