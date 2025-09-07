from state import State
from vector_search_helper.query_chroma_db import search_documents

def customer_support_rag_node(state: State):
    print("Routing to Customer Support RAG...")
    # mock routing logic
    search_query = state.search_query

    results = search_documents(search_query, num_results=3)
    print(f"Search results: {results}")

    results_str = "\n".join(results)

    state.messages.append({
        "role": "tool",
        "tool_call_id": state.tool_call_id,
        "content": results_str
    })

    return state