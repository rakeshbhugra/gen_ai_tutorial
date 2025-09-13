from state import State

def route_by_classification(state: State):
    if state.email_classification == "customer_support":
        return "customer_support_agent"
    elif state.email_classification == "sales":
        return "sales_agent"
    elif state.email_classification == "human_in_the_loop":
        return "human_in_the_loop"
    else:
        raise ValueError(f"Unknown classification: {state.email_classification}")
