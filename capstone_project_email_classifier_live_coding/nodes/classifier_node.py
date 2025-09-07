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
    system_prompt = """
    You are an email classification model. Classify the user's email into one of the following categories:
    1. customer_support
    2. sales
    3. human_in_the_loop (if the email is ambiguous and you cannot determine if it's customer_support or sales)
    
    example email: "I need help with my order."
    classification: customer_support
    
    example email: "Can you provide more information about your product pricing?"
    classification: sales
    
    example email: "hello, I have a question."
    classification: human_in_the_loop
    """

    messages_for_llm = [
        {"role": "system", "content": system_prompt},
        *state.messages
    ]

    response = completion(
        model = "openai/gpt-4.1-mini",
        messages = messages_for_llm,
        response_format=EmailClassification
    )

    json_content = response['choices'][0]['message']['content']
    parsed_response = json.loads(json_content)
    classification = EmailClassification(**parsed_response)

    print(f"Classification: {classification.category}")
    state.classification = classification.category
    
    return state
