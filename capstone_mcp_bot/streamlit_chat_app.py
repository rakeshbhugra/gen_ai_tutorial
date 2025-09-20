import streamlit as st
from mcp_bot_host import get_response

def main():
    """
    Main function that creates and runs the Streamlit chatbot interface
    
    This function sets up the web page configuration, manages the chat interface,
    handles user interactions, and maintains conversation state.
    """
    
    # Configure the Streamlit page
    # This must be the first Streamlit command and sets global page settings
    st.set_page_config(
        page_title="MCP Chatbot",    # Browser tab title
        page_icon="🤖",           # Browser tab icon
        layout="centered"         # Page layout style
    )
    
    # Create the page header
    st.title("MCP Chatbot")
    st.markdown("---")  # Horizontal line separator
    
    # Initialize chat history using Streamlit's session state
    # Session state persists data across user interactions and page refreshes
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your MCP Bot. How can I assist you today?"}
        ]

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
                response = get_response(st.session_state.messages)
            # Display without animation by using write
            st.write(response)
        
        # Step 4: Store AI response in conversation history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()