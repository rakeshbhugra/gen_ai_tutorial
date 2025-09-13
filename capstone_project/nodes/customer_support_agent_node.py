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
    print("Customer Support Agent node processing...")
    # Simulate some processing
    model = "openai/gpt-4.1-mini"
    response = litellm.completion(
        model=model,
        messages=state.messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        print(f"Model wants to call a tool...")
        print(f"Tool call: {response_message.tool_calls[0]}")
        state.messages.append(
            {
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": response_message.tool_calls
            }
        )
        state.next_node = "customer_support_rag"

    
    return state
