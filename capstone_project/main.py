from build_graph import build_graph
from visualize_graph import visualize_graph
from state import State

graph = build_graph()

# visualize_graph(graph, name="capstone_project_graph.png")

user_query = "Can you help me with signing in to my account?"
result = graph.invoke(State(
    messages=[{"role": "user", "content": user_query}]
))