import sys
from FlowGraph import FlowGraph, generate_random_flow_graph, prepare_multilayer_graph,draw_multilayer_graph_with_flow,\
    draw_multilayer_graph, ford_fulkerson


def draw_graph_with_flow() -> None:
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
        return_g = ford_fulkerson(flow_graph.flow_dict)
        residual_graph = prepare_multilayer_graph(return_g, flow_graph.layers)
        draw_multilayer_graph_with_flow(residual_graph, bool(int(save_to_file)), file_name)
    else:
        print("Wrong input, try again")
        draw_graph_with_flow()


def get_layers():
    layers = input("How many layers between source and sink do uou want? Number must be between 2 and 4\n")
    if layers in ["2","3","4"]:
        return int(layers)
    else:
        print("Wrong input, try again")
        return get_layers()


def draw_graph() -> None:
    layers = get_layers()
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
        multi_dict = generate_random_flow_graph(layers)
        graph = prepare_multilayer_graph(multi_dict[0], multi_dict[1])
        flow_graph.set_flow_dict(multi_dict[0])
        flow_graph.set_layers(multi_dict[1])
        draw_multilayer_graph(graph, bool(int(save_to_file)), file_name)
    else:
        print("Wrong input, try again")
        draw_graph()


def main() -> None:
    job = input("Select an option:\n"
                    "1 - Generate random flow graph\n"
                    )

    if job in ["1"]:
        if job == "1":
            draw_graph()
        while True:
            job = input("Choose what you want to do with the graph:\n"
                            "1 - Find max flow\n"
                            "2 - Exit the program\n"
                            "Press any other key to return to the main menu\n")
            if job in ["1", "2"]:
                if job == "1":
                    draw_graph_with_flow()
                if job == "2":
                    sys.exit(1)
            else:
                main()
    else:
        print("Wrong option selected, try again")
        main()


if __name__ == "__main__":
    flow_graph = FlowGraph()
    main()
