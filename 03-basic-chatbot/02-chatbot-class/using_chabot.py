# CHATBOT CLASS USAGE EXAMPLE
# This file demonstrates how to use the Chatbot class defined in 02_chatbot_class.py
# It shows proper instantiation, error handling, and user interaction patterns

# Import the Chatbot class from our local chatbot module
from .chatbot import Chatbot

# Create an instance of the Chatbot class
# We specify which AI model to use - in this case, Google's Gemini Flash model
chatbot = Chatbot(model_name="gemini/gemini-1.5-flash")

print("🤖 Chatbot initialized! Type 'exit' to end the conversation.")
print("=" * 50)

# Main conversation loop
while True:
    # Get user input with a clear prompt
    user_query = input("You: ")

    # Check for exit condition
    # Using .lower() makes the exit command case-insensitive
    if user_query.lower() == 'exit':
        print("👋 Goodbye! Thanks for chatting!")
        break

    # Use try-catch to handle potential errors gracefully
    try:
        # Call the chatbot's get_ai_response method
        # This method handles:
        # 1. Adding user message to history
        # 2. Making API call to AI model
        # 3. Adding AI response to history
        # 4. Returning the AI's response
        response = chatbot.get_ai_response(user_query)
        print("AI:", response)
        
    except ValueError as e:
        # Handle validation errors (e.g., empty messages)
        print(f"❌ Error: {e}")
        print("Please enter a valid message.")
        
    except Exception as e:
        # Handle any other unexpected errors
        print(f"❌ Unexpected error: {e}")
        print("Please try again or type 'exit' to quit.")

# BENEFITS OF THIS APPROACH:
# 
# 1. SEPARATION OF CONCERNS:
#    - Chatbot logic is in chatbot.py
#    - User interface logic is here
#    - Each file has a single responsibility
#
# 2. ERROR HANDLING:
#    - Catches specific errors (ValueError for validation)
#    - Catches general errors for unexpected issues
#    - Provides helpful error messages to users
#
# 3. USER EXPERIENCE:
#    - Clear prompts and feedback
#    - Graceful exit mechanism
#    - Continues running after errors
#
# 4. REUSABILITY:
#    - The Chatbot class can be used in different interfaces
#    - Easy to switch between models by changing the model_name
#    - Clean separation allows for easy testing