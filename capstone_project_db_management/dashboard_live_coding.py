import streamlit as st
import pandas as pd
from data_validation_live_coding import DataFrameValidator

def save_to_database(uploaded_df, filename):
    try:
        main_df_path = "capstone_project_db_management/database.xlsx"

        main_df = pd.read_excel(main_df_path)

        updated_df = pd.concat([main_df, uploaded_df])

        # write to excel file
        updated_df.to_excel(main_df_path, index=False)

        st.success(f"File '{filename}' saved to database successfully!")

    except:
        st.error("Error saving to database. Ensure the database file exists and is accessible.")


def handle_save_button_click(df, uploaded_file):
    validator = DataFrameValidator()

    try:
        validator.validate(df)
        st.success(f"File '{uploaded_file.name}' validated successfully!")

        save_to_database(df, uploaded_file.name)
        
    except ValueError as ve:
        st.error(f"Validation Error: {str(ve)}")
        return
    

def handle_file_upload(uploaded_file):
    # check file name
    if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        df = pd.read_excel(uploaded_file)
        st.subheader("Preview of uploaded file")
        st.dataframe(df)
        if st.button("Save to Database", type="primary"):
            handle_save_button_click(df, uploaded_file)
            
    else:
        st.error("Please upload a valid Excel file (.xlsx or .xls)")
        return

def upload_tab():
    st.header("Upload Data")
    st.write("This is the upload data tab.")
    uploaded_file = st.file_uploader("Upload your file here")
     
    if uploaded_file:
        handle_file_upload(uploaded_file)
    else:
        st.info("Awaiting file upload...")

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

if __name__ == "__main__":
    main()