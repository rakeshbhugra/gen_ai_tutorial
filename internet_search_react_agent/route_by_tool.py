from state import State
from langgraph.graph import END
from logger import logger

def route_by_tool(state: State):
    try:
        logger.info("Routing based on tool...")
        if state.next_node == "search":
            return "search"
        else:
            return END
    except Exception as e:
        logger.error(f"Error in route_by_tool: {e}")
        raise e