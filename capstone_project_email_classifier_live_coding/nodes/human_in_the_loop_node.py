from state import State

def human_in_the_loop_node(state: State):
    print("Routing to Human in the Loop...")
    # mock routing logic
    state.email_to = "supportagent@example.com"
    state.email_subject = "Response to your query"
    state.email_body = "Please help the user with their query."
    return state