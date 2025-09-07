from nodes import classifier_node
from state import State

query = "Can you help me with logging into my account?"
query = "I am looking to purch"

test_state = State(
    messages=[
        {"role": "user", "content":query}
    ]
)

updated_state = classifier_node(test_state)
print(updated_state.classification)