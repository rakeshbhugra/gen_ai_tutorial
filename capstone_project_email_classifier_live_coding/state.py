from pydantic import BaseModel

class State(BaseModel):
    messages: list[dict] = []
    classification: str | None = None
    next_node: str | None = None
    search_query: str | None = None
    email_to: str | None = None
    email_subject: str | None = None
    email_body: str | None = None
    tool_call_id: str | None = None