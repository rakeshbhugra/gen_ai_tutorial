import streamlit as st  

def main():
    st.set_page_config(
        page_title="MCP Chatbot",    # Browser tab title
        page_icon="🤖",           # Browser tab icon
        layout="centered"         # Page layout style
    )

    st.title("🤖 MCP Chatbot")
    st.markdown("---")  # Horizontal line separator

    if "messages" not in st.session_state:
        st.session_state.messages = []  # Empty list to store conversation history

    for message in st.session_state.messages:
        # Use Streamlit's chat_message component for proper styling
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    prompt = st.chat_input("Ask me anything...")
    
    if prompt:
        print("User prompt:", prompt)
    

if __name__ == "__main__":
    main()