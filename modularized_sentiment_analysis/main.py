from modularized_sentiment_analysis.state import State
from modularized_sentiment_analysis.state_graph import builder
from modularized_sentiment_analysis.visualize_graph import visualize_graph

graph = builder.compile()
visualize_graph(graph)
    
test_message = "I am having the best day of my life!"

initial_messages = [
    {"role": "user", "content": test_message}
]
initial_state = State(messages=initial_messages)


result = graph.invoke(initial_state)

print("final_output:", result)