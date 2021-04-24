from Graph import Graph
from GraphReader import IncorrectInputException
from GraphRepresentation import GraphRepresentation
from RandomGraphGenerator import BadNumberOfVertices
from RandomGraphGenerator import BadNumberOfEdges
from RandomGraphGenerator import BadProbability
import sys


graph = Graph()


def main():

    job = int(input("Select an option:\n"
                    "1 - Read the graph from file \n"
                    "2 - Generate a random graph \n"
                    ))

    if job in [1, 2]:
        if job == 1:
            if not read_graph():
                return 0
        if job == 2:
            if not generate_graph():
                print("An error occurred while generating the graph")
                return 0
        while True:
            job = int(input("Choose what you want to do with the graph:\n"
                            "1 - Save the graph to the file\n"
                            "2 - Print the graph\n"
                            "3 - Randomize graph edges\n"
                            "4 - Exit the program\n"))
            if job in [1, 2, 3, 4]:
                if job == 1:
                    if not save_graph():
                        print("An error occurred while saving the graph")
                    else:
                        print("Completed. Check folder data")
                if job == 2:
                    if not draw_graph():
                        print("An error occurred while printing the graph")
                if job == 3:
                    number_of_randomizations = int(input("Choose number of randomizations, zero for random in range 1-100:\n"))

                    if not randomize_graph(number_of_randomizations):
                        print("An error occurred while randomizing graph edges")

                if job == 4:
                    sys.exit(1)
            else:
                print("Wrong option selected, try again")
    else:
        print("Wrong option selected, try again")


def save_graph():
    representation = int(input("Select an output representation:\n"
                               "1 - Adjacency matrix\n"
                               "2 - Adjacency list\n"
                               "3 - Incidence matrix\n"
                               ))
    if representation in [1, 2, 3]:
        filename = input("Insert an output filename:\n")
        return graph.save_to_file(GraphRepresentation(representation), filename)
    else:
        print("Wrong representation selected, try again")
        return False


def draw_graph():
    save_to_file = int(input("Do you want to save image to a file? Select an option:\n"
                             "0 - No\n"
                             "1 - Yes\n"
                             ))
    if save_to_file in [0, 1]:
        graph.visualise_graph_on_circle(bool(save_to_file))
        return True


def generate_graph():
    graph_type = int(input("Select type of the graph:\n"
                           "1 - G(n,l)\n"
                           "2 - G(n,p)\n"
                           ))
    if graph_type in [1, 2]:
        n = int(input("Enter the number of graph vertices:\n"))
        if graph_type == 1:
            l = int(input("Enter the number of graph edges:\n"))
            try:
                graph.generate_NL_graph(n, l)
            except BadNumberOfEdges:
                print("enter correct number of edges please, now try again")
                generate_graph()
            except BadNumberOfVertices:
                print("Number of edges and vertices must be bigger than 1, now try again")
                generate_graph()
        if graph_type == 2:
            p = float(input("Enter the probability in range [0,1]:\n"))
            try:
                graph.generate_NP_graph(n, p)
            except BadProbability:
                print("Enter correct probability please, now try again")
                generate_graph()
            except BadNumberOfVertices:
                print("Number of edges and vertices must be bigger than 1, now try again")
                generate_graph()
        return True
    else:
        print("Wrong type of the graph selected")
        return False


def read_graph():
    try:
        representation = int(input("Enter a representation of the input\n"
                                   "1 - Adjacency matrix\n"
                                   "2 - Adjacency list\n"
                                   "3 - Incidence matrix\n"
                                   "4 - Graphical sequence\n"
                                   ))
        if representation in [1, 2, 3, 4]:
            filename = input("Enter the name of the input file (stored in folder data):\n")
            try:
                graph.read_data(GraphRepresentation(representation), filename)
            except IncorrectInputException as e:
                print(e.message)
                return False
        else:
            print("Wrong option selected")
            return False
    except ValueError as ve:
        print("Wrong option format: " + str(ve))
        return False
    return True


def randomize_graph(number_of_randomizations):
    return graph.randomize_graph_edges(number_of_randomizations)


if __name__ == "__main__":
    main()
