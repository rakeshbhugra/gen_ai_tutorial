from state import State

def customer_support_agent_node(state: State):
    print("Routing to Customer Support Agent...")
    # mock routing logic
    state.next_node = "send_email"
    return state