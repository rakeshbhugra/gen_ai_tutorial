from state import State

def route_by_classification(state: State):
    if state.classification == "sales":
        return "sales_agent"
    elif state.classification == "customer_support":
        return "customer_support_agent"
    else:
        return "human_in_the_loop"
