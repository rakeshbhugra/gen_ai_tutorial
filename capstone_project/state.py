from pydantic import BaseModel

class State(BaseModel):
    messages: list[dict] = []