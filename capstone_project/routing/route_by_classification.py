import sys
sys.path.append('..')
from state import State

def route_by_classification(state: State):
    last_message = state.messages[-1]["content"].lower()
    if "support" in last_message:
        return "customer_support_agent"
    elif "sales" in last_message:
        return "sales_agent"
    else:
        return "human_in_the_loop"