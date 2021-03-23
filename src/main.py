from src.Graph import Graph
from src.GraphRepresentation import GraphRepresentation

graph = Graph()

# GraphRepresentation(3) dla macierzy incydencji
graph.read_data(GraphRepresentation(3), "file.txt")

# z 3 na razie drukuje na sztywno - nie ma potrzeby wczytywania z pliku
print(graph.get_graph(GraphRepresentation(3)))

graph.save_to_file(GraphRepresentation(1), "out.txt")



#graph.print_graph_matrix()


# graph_reader = None
#
# print("Wybierz rodzaj reprezentacji, którą przekazujesz do programu")
# print("1) Macierz sąsiedztwa")
# print("2) Lista sąsiedztwa")
# print("3) Macierz incydencji")
#
# input_option = int(input(""))
# if input_option in [1, 2, 3]:
#     print("Wybierz rodzaj reprezentacji, którą chcesz otrzymać na wyjściu")
#     print("1) Macierz sąsiedztwa")
#     print("2) Lista sąsiedztwa")
#     print("3) Macierz incydencji")
#     output_option = int(input(""))
#     if output_option in [1, 2, 3]:
#         graph_reader = GraphReader(input_option, sys.argv[1])
#         if not graph_reader.read_input_data():
#             print("Niepoprawny plik wejściowy")
#         else:
#             print("Gitarka")
#             # graph_reader.export(output_option)
#
# if graph_reader is None:
#     print("Został podany zły numer")
#     sys.exit(1)