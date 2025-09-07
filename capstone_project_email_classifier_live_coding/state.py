from pydantic import BaseModel

class State(BaseModel):
    messages: list[dict] = []
    classification: str | None = None
    next_node: str | None = None