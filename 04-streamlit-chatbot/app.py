# STREAMLIT CHATBOT WITH GOOGLE GEMINI AI
# This is a complete web-based chatbot application using Streamlit and Google's Gemini AI
# It demonstrates modern web app development with AI integration

import streamlit as st          # Web framework for creating interactive apps
import google.generativeai as genai  # Google's Gemini AI SDK
import os                      # Operating system interface for environment variables
from dotenv import load_dotenv  # Load environment variables from .env file

# Load environment variables from .env file
# This is where we store sensitive information like API keys
load_dotenv()

# Configure Google Gemini AI with our API key
# The API key should be stored in a .env file as GOOGLE_API_KEY=your_key_here
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initialize the Gemini model
# 'gemini-2.5-flash' is a fast, efficient model good for chat applications
model = genai.GenerativeModel('gemini-2.5-flash')

def get_gemini_response(question: str) -> str:
    """
    Get a response from Google's Gemini AI model
    
    This function handles the AI API call and includes error handling
    for robust operation in a web environment.
    
    Args:
        question (str): The user's input question or prompt
        
    Returns:
        str: The AI's response text, or an error message if something went wrong
    """
    try:
        # Generate content using Gemini AI
        # The model processes the question and returns a response
        response = model.generate_content(question)
        return response.text
        
    except Exception as e:
        # Handle any errors that might occur during API call
        # This could be network issues, API key problems, rate limiting, etc.
        return f"Error: {str(e)}"

def main():
    """
    Main function that creates and runs the Streamlit chatbot interface
    
    This function sets up the web page configuration, manages the chat interface,
    handles user interactions, and maintains conversation state.
    """
    
    # Configure the Streamlit page
    # This must be the first Streamlit command and sets global page settings
    st.set_page_config(
        page_title="AI Chatbot",    # Browser tab title
        page_icon="🤖",           # Browser tab icon
        layout="centered"         # Page layout style
    )
    
    # Create the page header
    st.title("🤖 AI Chatbot")
    st.markdown("---")  # Horizontal line separator
    
    # Initialize chat history using Streamlit's session state
    # Session state persists data across user interactions and page refreshes
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Empty list to store conversation history
    
    # Display the entire chat history
    # This recreates the conversation each time the page refreshes
    for message in st.session_state.messages:
        # Use Streamlit's chat_message component for proper styling
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input widget at the bottom of the page
    # The walrus operator (:=) assigns the input to 'prompt' and checks if it's not empty
    if prompt := st.chat_input("Ask me anything..."):
        
        # Step 1: Store user message in conversation history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Step 2: Display the user's message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Step 3: Get and display the AI response
        with st.chat_message("assistant"):
            # Show a thinking spinner while waiting for AI response
            with st.spinner("Thinking..."):
                response = get_gemini_response(prompt)
                st.markdown(response)
        
        # Step 4: Store AI response in conversation history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Run the application
# This ensures main() only runs when the script is executed directly
# (not when imported as a module)
if __name__ == "__main__":
    main()

# KEY STREAMLIT CONCEPTS DEMONSTRATED:
#
# 1. SESSION STATE: st.session_state persists data across user interactions
# 2. CHAT COMPONENTS: st.chat_message() and st.chat_input() create chat UI
# 3. PAGE CONFIG: st.set_page_config() must be first Streamlit command
# 4. REACTIVITY: Page refreshes automatically when user interacts
# 5. WIDGETS: st.spinner() provides visual feedback during processing
# 6. LAYOUT: Streamlit handles responsive design automatically
#
# DEPLOYMENT NOTES:
# - Run with: streamlit run app.py
# - Access at: http://localhost:8501
# - Deploy to Streamlit Cloud, Heroku, or similar platforms
#
# SECURITY CONSIDERATIONS:
# - Never commit .env files to version control
# - Use Streamlit secrets management for production
# - Implement rate limiting for production use
# - Validate and sanitize user inputs
