from pydantic import BaseModel
from typing import Literal

class State(BaseModel):
    messages: list[dict] = []
    email_classification: Literal[
        "customer_support",
        "sales",
        "human_in_the_loop"
        ] | None = None

    next_node: str | None = None