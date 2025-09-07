import streamlit as st

def upload_tab():
    st.header("Upload Data")
    st.write("This is the upload data tab.")
    st.file_uploader("Upload your file here")

def chat_tab():
    st.header("Chat Assistant")
    st.write("This is the chat assistant tab.")

def main():
    st.title("Dashboard Live Coding Session")
    st.write("This is a live coding session for the dashboard.")

    tab1, tab2 = st.tabs([
        "Upload Data",
        "Chat Assistant",
    ])
    
    with tab1:
        upload_tab()

    with tab2:
        chat_tab()
    # st.file_uploader("Upload your file here")

if __name__ == "__main__":
    main()