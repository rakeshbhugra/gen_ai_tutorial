# create nodes - done
# create a graph - done
# create edges - done
# visualize the graph (optional) - done
# modularize the code - done
# fill in the functions with mock logic to test the flow - done
# fill in the functions with actual logic

from build_graph import graph
from visualize_graph import visualize_graph
from state import State

# visualize_graph(graph, "email_classifier_graph.png")

user_query = "Can you help me with logging into my account?"

init_messages = [
    {"role": "user", "content": user_query},
]

init_state = State(
    messages=init_messages
)

result = graph.invoke(
    init_state
)