from pydantic import BaseModel

# State
class State(BaseModel):
    messages: list[dict]
    search_results: str = ""