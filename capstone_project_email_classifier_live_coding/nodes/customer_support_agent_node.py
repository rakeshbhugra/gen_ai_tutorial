'''
Customer Support Agent has two tools:
1. Search on your documents
2. Send an email to the user
'''

from state import State
import litellm

def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for relevant information based on the query.
    
    Parameters
    ----------
    query : str
        The user's query or email content.  
        
    Returns
    -------
    str
        The relevant information found in the knowledge base.
    """

    return f"Search results for query: {query}"

def send_email(to: str, subject: str, body: str) -> str:
    """
    Simulate sending an email.
    
    Parameters
    ----------
    to : str
        The recipient's email address.
    subject : str
        The subject of the email.
    body : str
        The body content of the email.
    
    Returns
    -------
    str
        Confirmation message indicating the email was sent.
    """
    return f"Email sent to {to} with subject '{subject}'."
 
tools = [
    {"type": "function", "function": litellm.utils.function_to_dict(search_knowledge_base)},
    {"type": "function", "function": litellm.utils.function_to_dict(send_email)}
]


def customer_support_agent_node(state: State):
    print("Routing to Customer Support Agent...")
    # mock routing logic
    
    system_prompt = """
    You are a customer support agent. You always have to use one of the two tools:
    1. search_knowledge_base: to search for relevant information in the knowledge base.
    2. send_email: to send an email to the user.

    if the query is related to a specific product or service, use the search_knowledge_base tool to find relevant information.
    if the query is general or require more information from the user, use the send_email tool to respond to the user.
    """

    messages_for_llm = [
        {"role": "system", "content": system_prompt},
        *state.messages
    ]
    
    model = "openai/gpt-4.1-mini"
    response = litellm.completion(
        model=model,
        messages=messages_for_llm,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    print(f"Response Message: {response_message}")

    if response_message.tool_calls:
        state.messages.append(
            {
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": response_message.tool_calls
            }
        )

        if response_message.tool_calls[0]['name'] == 'search_knowledge_base':
            state.next_node = "customer_support_rag"
        elif response_message.tool_calls[0]['name'] == 'send_email':
            state.next_node = "send_email"
    else:
        raise ValueError("No tool call made by the model.")
    
    
    state.next_node = "send_email"
    return state