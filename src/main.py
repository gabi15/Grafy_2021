from Graph import Graph
from GraphRepresentation import GraphRepresentation
import sys


graph = Graph()

# GraphRepresentation(3) dla macierzy incydencji
#graph.read_data(GraphRepresentation(3), "file.txt")

# z 3 na razie drukuje na sztywno - nie ma potrzeby wczytywania z pliku
#print(graph.get_graph(GraphRepresentation(3)))

#graph.save_to_file(GraphRepresentation(1), "out.txt")


# dummy main function

def main():

    job = int(input("Select option:\n"
                    "1 - Read a graph from file \n"
                    "2 - Generate a random graph \n"
                    ))

    if job in [1, 2]:
        if job == 1:
            if not read_graph():
                print("Wystąpił błąd podczas odczytu pliku")
                return 0
        if job == 2:
            if not generate_graph():
                print("Wystąpił błąd podczas generowania grafu")
                return 0
        while True:
            job = int(input("Wybierz co chcesz zrobić z utworzonym grafem:\n"
                            "1 - Zapisz graf do pliku\n"
                            "2 - Narysuj graf\n"
                            "3 - Opuść program\n"))
            if job in [1, 2, 3]:
                if job == 1:
                    if not save_graph():
                        print("Wystąpił problem przy zapisie grafu")
                    else:
                        print("Udało się. Sprawdź folder data")
                if job == 2:
                    if not draw_graph():
                        print("Wystąpił błąd podczas rysowania grafu")
                if job == 3:
                    print("Zapraszamy ponownie")
                    sys.exit(1)
            else:
                print("Wybrano złą opcję, spróbuj ponownie")
    else:
        print("Zły wybór opcji, spróbuj jeszcze raz")


def save_graph():
    representation = int(input("Wybierz reprezentację do zapisu:\n"
                               "1 - Macierz sąsiedztwa\n"
                               "2 - Lista sąsiedztwa\n"
                               "3 - Macierz incydencji\n"
                               ))
    if representation in [1, 2, 3]:
        filename = input("Wybierz nazwę pliku wynikowego:\n")
        return graph.save_to_file(GraphRepresentation(representation), filename)
    else:
        print("Wybrano złą reprezentację")
        return False


def draw_graph():
    save_to_file = int(input("Czy chcesz zapisać obrazek do pliku? Wybierz odpowiednią opcję:\n"
                             "0 - Nie\n"
                             "1 - Tak\n"
                             ))
    if save_to_file in [0, 1]:
        graph.visualise_graph_on_circle(bool(save_to_file))
        return True


def generate_graph():
    graph_type = int(input("Wybierz rodzaj grafu, który chcesz wygenerować\n"
                           "1 - G(n,l)\n"
                           "2 - G(n,p)\n"
                           ))
    if graph_type in [1, 2]:
        n = int(input("Wprowadź liczbę wierzchołków grafu:\n"))
        if graph_type == 1:
            l = int(input("Wprowadź liczbę krawędzi grafu:\n"))
            graph.generate_NL_graph(n, l)
        if graph_type == 2:
            p = int(input("Wprowadź prawdopodobieństwo występowania krawędzi w zakresie [0,1]:\n"))
            graph.generate_NP_graph(n, p)
        return True
    else:
        print("Zły wybór typu grafu")
        return False


def read_graph():
    representation = int(input("Wybierz rodzaj reprezentacji, którą przekazujesz do programu\n"
                               "1 - Macierz sąsiedztwa\n"
                               "2 - Lista sąsiedztwa\n"
                               "3 - Macierz incydencji\n"
                               ))
    if representation in [1, 2, 3]:
        filename = input("Podaj nazwę pliku z danymi umieszczonym w folderze data:\n")
        return graph.read_data(GraphRepresentation(representation), filename)
    else:
        print("Podano złą komendę")
        return False


if __name__ == "__main__":
    main()
