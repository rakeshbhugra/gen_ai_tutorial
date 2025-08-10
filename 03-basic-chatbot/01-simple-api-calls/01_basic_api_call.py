# MOST BASIC LITELLM CHATBOT
# This is the simplest possible chatbot using the LiteLLM library
# It demonstrates the core concepts without any classes or complex structure

# Suppress LiteLLM debug logs to keep output clean
import os; os.environ['LITELLM_LOG'] = 'CRITICAL'

# Import the completion function from LiteLLM
# LiteLLM allows us to call different AI models with a unified interface
from litellm import completion

# Initialize conversation history with a system message
# The system message sets the personality/behavior of the AI
conversation_history = [
    {"role": "system", "content": "You are a judgy person, you always response with a sarcastic tone."},
]

# Main chat loop
while True:
    # Get user input
    user_input = input("User: ")
    
    # Add user message to conversation history
    # Each message needs a "role" (user/assistant/system) and "content"
    conversation_history.append({"role": "user", "content": user_input})

    # Call the AI model
    # - model: specifies which AI model to use (Gemini in this case)
    # - messages: the full conversation history
    # - api_key: authentication (should use environment variables in production)
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=conversation_history,
        api_key=""  # TODO: Add your actual API key or use environment variable
    )

    # Extract the AI's response from the API response
    # The response structure: response['choices'][0]['message']['content']
    ai_response = response['choices'][0]['message']['content']
    print("AI:", ai_response)
    
    # Add AI response to conversation history to maintain context
    # This allows the AI to remember previous parts of the conversation
    conversation_history.append({"role": "assistant", "content": ai_response})

# IMPORTANT CONCEPTS DEMONSTRATED:
# 1. Conversation History: Maintaining context across multiple exchanges
# 2. Message Roles: system, user, assistant have different purposes
# 3. API Integration: How to call AI models through LiteLLM
# 4. Continuous Loop: Interactive chat experience

# SECURITY NOTE: Never hardcode API keys in production code!
# Use environment variables: os.getenv('GEMINI_API_KEY')
