from state import State

def classifier_node(state: State):
    last_message = state.messages[-1]['content']
    if "sales" in last_message.lower():
        state.classification = "sales_agent"

    elif "support" in last_message.lower():
        state.classification = "customer_support_agent"

    else:
        state.classification = "human_in_the_loop"
    print("Classifying email...")
    # mock classification logic
    return state