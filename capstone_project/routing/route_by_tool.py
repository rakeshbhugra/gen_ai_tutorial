import sys
sys.path.append('..')
from state import State

def route_by_tool(state: State):
    last_user_message = state.messages[-1]["content"].lower()
    if "send_email" in last_user_message:
        return "send_email"
    else:
        return "RAG"