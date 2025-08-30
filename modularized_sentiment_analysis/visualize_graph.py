def visualize_graph(graph):
    # Visualize the graph
    try:
        png_data = graph.get_graph(xray=True).draw_mermaid_png()
        with open("conditional_edge_graph.png", "wb") as f:
            f.write(png_data)
        print("Graph diagram saved as 'conditional_edge_graph.png'")
    except Exception as e:
        print(f"Could not generate graph image: {e}")
