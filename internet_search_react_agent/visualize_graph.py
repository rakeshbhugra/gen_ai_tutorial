from logger import logger

def visualize_graph(graph, name):
    try:
        png_data = graph.get_graph(xray=True).draw_mermaid_png()
        with open(name, "wb") as f:
            f.write(png_data)
        logger.info(f"Graph diagram saved as '{name}'")
    except Exception as e:
        logger.error(f"Could not generate graph image: {e}")