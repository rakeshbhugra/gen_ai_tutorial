from pydantic import BaseModel

# State
class State(BaseModel):
    messages: list[dict]
    next_node: str|None  = None
    search_results: str = ""
    search_query: str = ""