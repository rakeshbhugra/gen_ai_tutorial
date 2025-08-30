from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel
from litellm import completion
from typing import Literal
import json

class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]

class State(BaseModel):
    messages: list[dict]
    sentiment: str = "neutral"
    
# Define nodes
def analyze_sentiment(state: State):
    print("Analyzing sentiment...")

    response = completion(
        model="openai/gpt-4.1-mini",
        messages=state.messages,
        response_format=SentimentResponse
    )

    json_content = response.choices[0].message.content
    json_dict = json.loads(json_content)
    sentiment_respone = SentimentResponse(**json_dict)

    state.sentiment = sentiment_respone.sentiment

    return state

def positive_response(state: State):
    print("Generating positive response...")
    print("Thank you for sharing your positive thoughts!")
    return state
    
def negative_response(state: State):
    print("Generating negative response...")
    print("I'm sorry to hear that. How can I assist you further?")
    return state

def neutral_response(state: State):
    print("Generating neutral response...")
    print("I see. Please tell me more.")
    return state

# conditional edge routing function
def route_by_sentiment(state: State):
    print(f"Routing based on sentiment: {state.sentiment}")
    if state.sentiment == "positive":
        return "positive_node"
    elif state.sentiment == "negative":
        return "negative_node"
    else:
        return "neutral_node"
    
    
# Creating the graph
builder = StateGraph(State)


# Adding nodes
builder.add_node("analyze_sentiment", analyze_sentiment)
builder.add_node("positive_node", positive_response)
builder.add_node("negative_node", negative_response)
builder.add_node("neutral_node", neutral_response)


# Add edges
builder.add_edge(START, "analyze_sentiment")

# Add conditional edge
builder.add_conditional_edges(
    "analyze_sentiment",
    route_by_sentiment,
    {
        "positive_node": "positive_node",
        "negative_node": "negative_node",
        "neutral_node": "neutral_node"
    }
)


# Connecting all the response nodes to END
builder.add_edge("positive_node", END)
builder.add_edge("negative_node", END)
builder.add_edge("neutral_node", END)

graph = builder.compile()

# Visualize the graph
try:
    png_data = graph.get_graph(xray=True).draw_mermaid_png()
    with open("conditional_edge_graph.png", "wb") as f:
        f.write(png_data)
    print("Graph diagram saved as 'conditional_edge_graph.png'")
except Exception as e:
    print(f"Could not generate graph image: {e}")

    
test_message = "I am not having a good day"

initial_messages = [
    {"role": "user", "content": test_message}
]
initial_state = State(messages=initial_messages)


result = graph.invoke(initial_state)

print("final_output:", result)