from state import State

def route_by_classification(state: State):
    # mock routing logic based on classification
    if state.classification == "sales_agent":
        return "sales_agent"
    elif state.classification == "customer_support_agent":
        return "customer_support_agent"
    else:
        return "human_in_the_loop"
