def visualize_graph(graph, name):
    try:
        png_data = graph.get_graph(xray=True).draw_mermaid_png()
        with open(name, "wb") as f:
            f.write(png_data)
        print(f"Graph diagram saved as '{name}'")
    except Exception as e:
        print(f"Could not generate graph image: {e}")