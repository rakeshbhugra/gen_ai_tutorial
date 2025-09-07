from state import State
import litellm
from pydantic import BaseModel
from typing import Literal
import json

class EmailClassificationResponse(BaseModel):
    classification: Literal["customer_support", "sales", "human_in_the_loop"]

def email_classifier_node(state: State):
    print("Email Classifier node processing...")
    model = "gpt-4.1-mini"
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
    
    messages_for_classification = [
        {"role": "system", "content": system_prompt},
        *state.messages
    ]
    response = litellm.completion(
        model = model,
        messages=messages_for_classification,
        response_format=EmailClassificationResponse
    )

    # print('response:', response)
    classification = response.choices[0].message.content
    classification_json = json.loads(classification)
    state.email_classification = classification_json['classification']
    print(f"Email classified as: {classification_json['classification']}")
    return state

if __name__ == "__main__":
    result = email_classifier_node(State(messages=[{"role": "user", "content": "I need help with my order."}]))