from state import State

def sales_agent_node(state: State):
    print("Routing to Sales Agent...")
    # mock routing logic
    state.next_node = "send_email"
    return state