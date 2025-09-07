from state import State
from pydantic import BaseModel
from typing import Literal
from litellm import completion
import json

class EmailClassification(BaseModel):
    category: Literal["customer_support", "sales", "human_in_the_loop"]

def classifier_node(state: State):
    print("Classifying email...")

    # use LLM to classify the email into one of the categories
    # customer_support, sales, human_in_the_loop

    response = completion(
        model = "openai/gpt-4.1-mini",
        messages = state.messages,
        response_format=EmailClassification
    )

    json_content = response['choices'][0]['message']['content']
    parsed_response = json.loads(json_content)
    classification = EmailClassification(**parsed_response)

    print(f"Classification: {classification.category}")
    state.classification = classification.category
    
    return state
