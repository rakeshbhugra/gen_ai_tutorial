from langgraph.graph import START, END, StateGraph
from modularized_sentiment_analysis.state import State
from modularized_sentiment_analysis.nodes.analyze_sentiment import analyze_sentiment
from modularized_sentiment_analysis.nodes.positive_response import positive_response
from modularized_sentiment_analysis.nodes.negative_response import negative_response
from modularized_sentiment_analysis.nodes.neutral_response import neutral_response

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