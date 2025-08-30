from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel

class State(BaseModel):
    messages: list[dict]

# define nodes
def chatbot_node(state: State):
    """Simulate a chatbot response"""
    print("Chatbot node processing...")
    user_message = state.messages[-1]["content"]
    bot_response = f"Echo: {user_message}"
    state.messages.append({"role": "assistant", "content": bot_response})
    return state

builder = StateGraph(State)

builder.add_node("chatbot", chatbot_node)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)


graph = builder.compile()

try:
    # Save the image to file
    png_data = graph.get_graph(xray=True).draw_mermaid_png()
    with open("react_agent_graph.png", "wb") as f:
        f.write(png_data)
    print("Graph diagram saved as 'react_agent_graph.png'")
    
except Exception as e:
    print(f"Could not generate graph image: {e}")


initial_messages = [
    {"role": "user", "content": "Hello, how are you?"}
]

initial_state = State(messages=initial_messages)

result = graph.invoke(initial_state)

print("final_output:", result)
