# LITELLM COMPLETION API DEMONSTRATION
# This file shows how to use LiteLLM's completion API with different approaches
# It demonstrates both single-shot and conversational AI interactions

from litellm import completion

# Initialize the conversation with a system message
# System messages define the AI's role, personality, and behavior guidelines
messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
]

# EXAMPLE 1: Single Query Approach (commented out for now)
# This shows how to make a single API call without a conversation loop

# Get user input
# user_query = input("Enter your query: ")

# Add user message to the messages list
# messages.append({'role': 'user', 'content': user_query})

# Debug: Show the message structure before sending to API
# print(messages)

# Make API call to get AI response
# response = completion(
#     model = "gemini/gemini-1.5-flash",  # Google's Gemini model
#     # model = "ollama/llama3:latest",   # Alternative: local Ollama model
#     messages = messages,
#     api_key='YOUR_API_KEY_HERE'         # SECURITY: Use environment variables!
# )

# Extract and display the AI's response
# print("AI Response:", response['choices'][0]['message']['content'])

# EXAMPLE 2: Conversational Chat Loop
# This approach maintains conversation history for context-aware responses

while True:
    # Get user input
    user_query = input("You: ")
    
    # Exit condition - allow user to end the conversation gracefully
    if user_query.lower() == 'exit':
        print("👋 Goodbye!")
        break
    
    # Add user message to conversation history
    messages.append({'role': 'user', 'content': user_query})
    
    # Make API call with full conversation history
    # This allows the AI to maintain context across multiple exchanges
    response = completion(
        model = "gemini/gemini-1.5-flash",  # Specify the AI model to use
        messages = messages,                 # Send entire conversation history
        api_key='...'                       # TODO: Replace with actual API key
    )
    
    # Extract AI response from the API response object
    ai_response = response['choices'][0]['message']['content']
    print("AI:", ai_response)
    
    # Add AI response to conversation history
    # This is crucial for maintaining conversational context
    messages.append({'role': 'assistant', 'content': ai_response})

# KEY CONCEPTS EXPLAINED:
# 
# 1. MESSAGE ROLES:
#    - 'system': Sets AI behavior and personality
#    - 'user': Messages from the human user
#    - 'assistant': Messages from the AI
#
# 2. CONVERSATION HISTORY:
#    - Each API call sends the entire conversation
#    - Allows AI to reference previous messages
#    - Context window limitations apply (model-dependent)
#
# 3. API RESPONSE STRUCTURE:
#    - response['choices'] contains possible completions
#    - response['choices'][0]['message']['content'] has the actual text
#
# 4. MODEL SELECTION:
#    - Different models have different capabilities and costs
#    - LiteLLM supports many providers: OpenAI, Anthropic, Google, etc.
#
# 5. SECURITY BEST PRACTICES:
#    - Never hardcode API keys in source code
#    - Use environment variables: os.getenv('API_KEY')
#    - Consider rate limiting and usage monitoring