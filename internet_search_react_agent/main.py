import json
from build_graph import build_graph
from state import State

graph = build_graph()

query = "find me information about LangGraph and its use cases."
# query = "Hello"
# query = "News"
init_messages = [
    {"role": "user", "content": query}
]

init_state = State(messages=init_messages)

final_state = graph.invoke(init_state)
# print("Final state:", final_state)
# print("Pretty print:", json.dumps(final_state, indent=2))