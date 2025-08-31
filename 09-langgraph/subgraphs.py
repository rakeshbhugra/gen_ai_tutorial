"""
Proper Subgraphs Tutorial - Following LangGraph Documentation
This example shows the correct way to combine subgraphs by adding compiled graphs as nodes
"""

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from litellm import completion
from typing import Literal, List
import json

load_dotenv()

# ============= SHARED STATE DEFINITION =============
# Both parent and subgraphs share compatible state schemas
class SharedState(TypedDict):
    messages: List[dict]
    sentiment: str
    calculation_result: str
    user_query: str

# ============= SENTIMENT SUBGRAPH =============
class SentimentResponse(TypedDict):
    sentiment: Literal["positive", "negative", "neutral"]

def analyze_sentiment(state: SharedState):
    print("  [Sentiment Subgraph] Analyzing sentiment...")
    
    # Use JSON schema for litellm
    response = completion(
        model="openai/gpt-4o-mini",
        messages=state["messages"] + [{"role": "system", "content": "Analyze the sentiment and respond with JSON: {\"sentiment\": \"positive\" | \"negative\" | \"neutral\"}"}],
        response_format={"type": "json_object"}
    )
    
    json_content = response.choices[0].message.content
    json_dict = json.loads(json_content)
    
    return {"sentiment": json_dict.get("sentiment", "neutral")}

def positive_response(state: SharedState):
    print("  [Sentiment Subgraph] Generating positive response...")
    return {"messages": state["messages"] + [{"role": "assistant", "content": "Great to hear you're positive! 😊"}]}

def negative_response(state: SharedState):
    print("  [Sentiment Subgraph] Generating negative response...")
    return {"messages": state["messages"] + [{"role": "assistant", "content": "I'm sorry you're feeling down. 😔"}]}

def neutral_response(state: SharedState):
    print("  [Sentiment Subgraph] Generating neutral response...")
    return {"messages": state["messages"] + [{"role": "assistant", "content": "I understand. Tell me more. 😐"}]}

def route_by_sentiment(state: SharedState):
    if state["sentiment"] == "positive":
        return "positive_node"
    elif state["sentiment"] == "negative":
        return "negative_node"
    else:
        return "neutral_node"

# Build sentiment subgraph
sentiment_builder = StateGraph(SharedState)
sentiment_builder.add_node("analyze", analyze_sentiment)
sentiment_builder.add_node("positive_node", positive_response)
sentiment_builder.add_node("negative_node", negative_response)
sentiment_builder.add_node("neutral_node", neutral_response)

sentiment_builder.add_edge(START, "analyze")
sentiment_builder.add_conditional_edges(
    "analyze",
    route_by_sentiment,
    {
        "positive_node": "positive_node",
        "negative_node": "negative_node",
        "neutral_node": "neutral_node"
    }
)
sentiment_builder.add_edge("positive_node", END)
sentiment_builder.add_edge("negative_node", END)
sentiment_builder.add_edge("neutral_node", END)

# Compile sentiment subgraph
sentiment_subgraph = sentiment_builder.compile()

# ============= CALCULATOR SUBGRAPH =============
import litellm

def sum_numbers(a: float, b: float) -> float:
    """Add two numbers together"""
    return a + b

def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

TOOLS = [
    {"type": "function", "function": litellm.utils.function_to_dict(sum_numbers)},
    {"type": "function", "function": litellm.utils.function_to_dict(multiply_numbers)},
]

FUNCTION_MAP = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
}

def calculator_reasoner(state: SharedState):
    print("  [Calculator Subgraph] Processing calculation request...")
    
    response = litellm.completion(
        model="gpt-4o-mini",
        messages=state["messages"],
        tools=TOOLS,
        tool_choice="auto",
    )
    
    response_message = response.choices[0].message
    
    if response_message.tool_calls:
        # Execute tool calls
        results = []
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            print(f"    Calling {function_name} with {function_args}")
            
            result = FUNCTION_MAP[function_name](**function_args)
            results.append(str(result))
        
        return {"calculation_result": f"Calculation: {', '.join(results)}"}
    else:
        return {"calculation_result": response_message.content or "No calculation needed"}

# Build calculator subgraph
calculator_builder = StateGraph(SharedState)
calculator_builder.add_node("calculate", calculator_reasoner)
calculator_builder.add_edge(START, "calculate")
calculator_builder.add_edge("calculate", END)

# Compile calculator subgraph
calculator_subgraph = calculator_builder.compile()

# ============= PARENT ORCHESTRATOR GRAPH =============
def prepare_state(state: SharedState):
    """Prepare initial state from user query"""
    print(f"[Orchestrator] Processing query: {state['user_query']}")
    
    # Initialize messages from user query
    if not state.get("messages"):
        state["messages"] = [{"role": "user", "content": state["user_query"]}]
    
    return state

def combine_results(state: SharedState):
    """Combine results from subgraphs"""
    print("[Orchestrator] Combining results...")
    
    result_parts = []
    
    if state.get("sentiment"):
        emoji = {"positive": "😊", "negative": "😔", "neutral": "😐"}.get(state["sentiment"], "")
        result_parts.append(f"Sentiment: {emoji} {state['sentiment']}")
    
    if state.get("calculation_result"):
        result_parts.append(state["calculation_result"])
    
    final_message = " | ".join(result_parts) if result_parts else "Processing complete"
    
    return {"messages": state["messages"] + [{"role": "assistant", "content": final_message}]}

def should_calculate(state: SharedState):
    """Determine if calculation is needed"""
    query_lower = state["user_query"].lower()
    math_keywords = ["calculate", "add", "multiply", "sum", "product", "what is", "+", "*"]
    
    if any(keyword in query_lower for keyword in math_keywords):
        return "calculator"
    return "combine"

# Build parent orchestrator - ADDING COMPILED SUBGRAPHS AS NODES
orchestrator_builder = StateGraph(SharedState)

# Add regular nodes
orchestrator_builder.add_node("prepare", prepare_state)
orchestrator_builder.add_node("combine", combine_results)

# ADD COMPILED SUBGRAPHS DIRECTLY AS NODES - This is the key!
orchestrator_builder.add_node("sentiment_analysis", sentiment_subgraph)
orchestrator_builder.add_node("calculator", calculator_subgraph)

# Add edges
orchestrator_builder.add_edge(START, "prepare")
orchestrator_builder.add_edge("prepare", "sentiment_analysis")

# Conditional routing after sentiment
orchestrator_builder.add_conditional_edges(
    "sentiment_analysis",
    should_calculate,
    {
        "calculator": "calculator",
        "combine": "combine"
    }
)

orchestrator_builder.add_edge("calculator", "combine")
orchestrator_builder.add_edge("combine", END)

# Compile the parent graph
orchestrator_graph = orchestrator_builder.compile()

# ============= TEST THE ORCHESTRATOR =============
if __name__ == "__main__":
    print("="*60)
    print("🎯 PROPER SUBGRAPHS IMPLEMENTATION")
    print("="*60)
    print("Key difference: Compiled subgraphs are added directly as nodes!")
    print("="*60)
    
    # Visualize the graph
    try:
        png_data = orchestrator_graph.get_graph(xray=True).draw_mermaid_png()
        with open("proper_subgraphs.png", "wb") as f:
            f.write(png_data)
        print("\n📊 Graph diagram saved as 'proper_subgraphs.png'")
    except Exception as e:
        print(f"Could not generate graph image: {e}")
    
    # Test cases
    test_cases = [
        "I'm having a wonderful day!",
        "What is 25 + 17?",
        "I'm upset that 10 * 5 isn't 100",
        "Tell me about the weather"
    ]
    
    print("\n" + "="*60)
    print("RUNNING TEST CASES")
    print("="*60)
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: '{query}'")
        print("="*60)
        
        try:
            initial_state = SharedState(
                user_query=query,
                messages=[],
                sentiment="",
                calculation_result=""
            )
            
            result = orchestrator_graph.invoke(initial_state)
            
            # Show final message
            final_message = result["messages"][-1]["content"] if result["messages"] else "No response"
            print(f"\n✅ Final Response: {final_message}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-"*60)