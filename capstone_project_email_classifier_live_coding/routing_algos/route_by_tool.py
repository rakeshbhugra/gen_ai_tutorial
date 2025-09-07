from state import State

def route_by_tool(state: State):
    if state.next_node == 'send_email':
        return "send_email"
    else:
        return "RAG"