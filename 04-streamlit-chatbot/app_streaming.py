# STREAMLIT CHATBOT WITH STREAMING RESPONSES
# This advanced version demonstrates real-time streaming of AI responses
# The user sees the AI response being "typed" in real-time, like ChatGPT

# Suppress LiteLLM debug logs to keep output clean
import os; os.environ['LITELLM_LOG'] = 'CRITICAL'

import streamlit as st          # Web framework for creating interactive apps
from litellm import completion  # Unified interface for multiple AI models
import time                    # Time utilities for controlling stream speed
from dotenv import load_dotenv  # Load environment variables from .env file

# Load environment variables from .env file
# This is where we store sensitive information like API keys
load_dotenv()

def get_ai_response_stream(question: str):
    """
    Get a streaming response from AI model using LiteLLM
    
    This function uses LiteLLM's streaming capability to receive the response
    in chunks as it's being generated, allowing for real-time display.
    
    Args:
        question (str): The user's input question or prompt
        
    Yields:
        str: Chunks of the AI response as they become available
    """
    try:
        # Generate content with streaming enabled
        # stream=True tells LiteLLM to send response chunks as they're generated
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": question}],
            stream=True
        )
        
        # Iterate through each chunk as it arrives
        for chunk in response:
            # Extract the content from the chunk
            # LiteLLM streaming returns delta content in choices[0].delta.content
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        # Handle any errors that might occur during streaming
        yield f"Error: {str(e)}"

def main():
    """
    Main function that creates the streaming chatbot interface
    
    This version includes advanced UI features like streaming responses
    and dynamic placeholders for better user experience.
    """
    
    # Configure the Streamlit page
    st.set_page_config(
        page_title="AI Chatbot (Streaming)",    # Browser tab title
        page_icon="🤖",                        # Browser tab icon
        layout="centered"                       # Page layout style
    )
    
    # Create the page header
    st.title("🤖 AI Chatbot (Streaming)")
    st.markdown("---")  # Horizontal line separator
    
    # Initialize chat history using Streamlit's session state
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Empty list to store conversation history
    
    # Display the entire chat history
    # Previous messages are shown normally (not streamed again)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input widget at the bottom of the page
    if prompt := st.chat_input("Ask me anything..."):
        
        # Step 1: Store and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Step 2: Display assistant response with streaming
        with st.chat_message("assistant"):
            
            # Create a placeholder for the "Thinking..." indicator
            # st.empty() creates a container that can be dynamically updated
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("Thinking...")
            
            # Define a generator function for the streaming response
            def response_generator():
                """
                Generator function that yields response chunks with timing control
                This creates the typewriter effect in the UI
                """
                first_chunk = True
                
                # Get chunks from the AI model
                for chunk in get_ai_response_stream(prompt):
                    # Remove the "Thinking..." indicator when first chunk arrives
                    if first_chunk:
                        thinking_placeholder.empty()
                        first_chunk = False
                    
                    # Yield the chunk for display
                    yield chunk
                    
                    # Small delay between chunks for smoother animation
                    # This controls the "typing speed" of the response
                    time.sleep(0.01)  # 10ms delay between characters/chunks
            
            # Use Streamlit's write_stream to display the streaming response
            # This creates the real-time typing effect
            full_response = st.write_stream(response_generator)
        
        # Step 3: Store the complete response in chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Run the application
if __name__ == "__main__":
    main()

# STREAMING CONCEPTS DEMONSTRATED:
#
# 1. STREAMING RESPONSES: AI response arrives in real-time chunks
# 2. DYNAMIC PLACEHOLDERS: st.empty() allows updating UI elements
# 3. GENERATOR FUNCTIONS: Python generators for efficient streaming
# 4. TIMING CONTROL: time.sleep() controls streaming speed
# 5. USER EXPERIENCE: Visual feedback with "Thinking..." indicator
# 6. REAL-TIME UI: st.write_stream() creates typewriter effect
#
# BENEFITS OF STREAMING:
# - Better user experience with immediate feedback
# - Perceived faster response times
# - Ability to stop generation early if needed
# - More engaging and interactive feel
# - Similar to ChatGPT and modern AI interfaces
#
# TECHNICAL NOTES:
# - Uses LiteLLM for unified model interface with streaming support
# - Uses Python generators for memory efficiency
# - Streamlit's write_stream handles the UI updates automatically
# - Full response is still stored in session state for history