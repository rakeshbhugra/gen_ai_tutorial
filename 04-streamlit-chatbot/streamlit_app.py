# STREAMLIT CHATBOT USING CUSTOM CHATBOT CLASS
# This version integrates our custom ChatBot class with Streamlit
# It demonstrates how to combine backend AI logic with frontend UI

import streamlit as st        # Web framework for creating interactive apps
from chat_bot import ChatBot  # Our custom ChatBot class from previous module
from dotenv import load_dotenv  # Load environment variables

# Load environment variables from .env file
# This ensures API keys and configuration are available
load_dotenv()

# Initialize the chatbot instance using Streamlit's session state
# Session state ensures the same chatbot instance persists across page interactions
if "chatbot" not in st.session_state:
    # Create a new ChatBot instance with local Ollama model
    # ollama/llama3:latest runs locally and doesn't require API keys
    st.session_state.chatbot = ChatBot(model_name="ollama/llama3:latest")
    
    # Set up the AI's personality with a system message
    # This defines how the AI should behave in conversations
    st.session_state.chatbot.add_message("system", "You are a helpful assistant.")

# Initialize chat message history for the UI display
# This is separate from the chatbot's internal history
# The UI history stores messages in Streamlit's expected format
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page header and description
st.title("AI Chatbot")
st.write("Chat with an AI assistant powered by Llama 3")

# Display all previous chat messages
# This recreates the conversation interface on each page load
for message in st.session_state.messages:
    # Use Streamlit's chat_message component for proper styling
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main chat input interface
# The walrus operator (:=) captures input and checks if it exists
if prompt := st.chat_input("What would you like to know?"):
    
    # Step 1: Add user message to UI history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Step 2: Get AI response using our custom ChatBot class
    with st.chat_message("assistant"):
        # Show spinner while waiting for AI response
        with st.spinner("Thinking..."):
            # Call our ChatBot's answer method
            # This handles the AI API call and conversation management
            response = st.session_state.chatbot.answer(prompt)
            st.markdown(response)
    
    # Step 3: Add AI response to UI history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Additional UI feature: Clear conversation button
# This provides a way to start fresh conversations
if st.button("Clear Chat"):
    # Clear the UI message history
    st.session_state.messages = []
    
    # Create a new ChatBot instance to reset conversation state
    st.session_state.chatbot = ChatBot(model_name="ollama/llama3:latest")
    st.session_state.chatbot.add_message("system", "You are a helpful assistant.")
    
    # Force Streamlit to refresh the page to reflect changes
    st.rerun()

# KEY INTEGRATION CONCEPTS DEMONSTRATED:
#
# 1. BACKEND-FRONTEND SEPARATION: 
#    - ChatBot class handles AI logic
#    - Streamlit handles UI and user interaction
#
# 2. SESSION STATE MANAGEMENT:
#    - Persistent chatbot instance across interactions
#    - Separate UI history for display purposes
#
# 3. LOCAL AI MODEL USAGE:
#    - Uses Ollama for local, private AI inference
#    - No external API keys required for basic functionality
#
# 4. USER EXPERIENCE FEATURES:
#    - Clear chat functionality for fresh starts
#    - Loading spinners for visual feedback
#    - Proper message formatting and display
#
# 5. ARCHITECTURE BENEFITS:
#    - Reusable ChatBot class across different interfaces
#    - Clean separation of concerns
#    - Easy to switch between different AI models
#    - Testable backend logic separate from UI
#
# LOCAL MODEL SETUP (OLLAMA):
# 1. Install Ollama: https://ollama.ai/
# 2. Pull Llama 3 model: ollama pull llama3
# 3. Start Ollama service: ollama serve
# 4. Run this app: streamlit run streamlit_app.py
#
# ALTERNATIVE MODELS:
# - Replace "ollama/llama3:latest" with:
#   - "gemini/gemini-1.5-flash" (requires GOOGLE_API_KEY)
#   - "openai/gpt-3.5-turbo" (requires OPENAI_API_KEY)
#   - "ollama/mistral" (local alternative model)