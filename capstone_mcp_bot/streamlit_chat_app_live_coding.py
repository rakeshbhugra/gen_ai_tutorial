import streamlit as st
from litellm import completion
from dotenv import load_dotenv

def get_response(messages: list[dict]) -> str:
    model = 'openai/gpt-4.1-mini'
    response = completion(
        model=model,
        messages=messages,
    )

    return response.choices[0].message['content']

def main():
    st.set_page_config(
        page_title="MCP Chatbot",    # Browser tab title
        page_icon="🤖",           # Browser tab icon
        layout="centered"         # Page layout style
    )

    st.title("🤖 MCP Chatbot")
    st.markdown("---")  # Horizontal line separator

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! How can I assist you today?"}
        ]  # Empty list to store conversation history

    for message in st.session_state.messages:
        # Use Streamlit's chat_message component for proper styling
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    prompt = st.chat_input("Ask me anything...")
    
    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = get_response(st.session_state.messages)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()