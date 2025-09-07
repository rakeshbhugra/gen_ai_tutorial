import streamlit as st
import pandas as pd
import os
from datetime import datetime

DB_FILE = "capstone_project_db_management/database.xlsx"

def load_database():
    if os.path.exists(DB_FILE):
        return pd.read_excel(DB_FILE)
    return pd.DataFrame()

def save_to_database(uploaded_df, filename):
    db_df = load_database()
    
    uploaded_df['source_file'] = filename
    uploaded_df['upload_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not db_df.empty and 'Customer ID' in db_df.columns and 'Customer ID' in uploaded_df.columns:
        existing_ids = set(db_df['Customer ID'].astype(str))
        new_records = uploaded_df[~uploaded_df['Customer ID'].astype(str).isin(existing_ids)]
        duplicate_records = uploaded_df[uploaded_df['Customer ID'].astype(str).isin(existing_ids)]
        
        if not duplicate_records.empty:
            st.warning(f"Found {len(duplicate_records)} duplicate Customer IDs that were skipped: {', '.join(duplicate_records['Customer ID'].astype(str).tolist())}")
        
        if not new_records.empty:
            updated_db = pd.concat([db_df, new_records], ignore_index=True)
            updated_db.to_excel(DB_FILE, index=False)
            return updated_db, len(new_records), len(duplicate_records)
        else:
            return db_df, 0, len(duplicate_records)
    else:
        updated_db = pd.concat([db_df, uploaded_df], ignore_index=True)
        updated_db.to_excel(DB_FILE, index=False)
        return updated_db, len(uploaded_df), 0


def handle_save_button_click(df, uploaded_file):
    updated_db, new_count, duplicate_count = save_to_database(df, uploaded_file.name)
    if new_count > 0:
        st.success(f"Successfully added {new_count} new records to database!")
    if duplicate_count > 0:
        st.info(f"Skipped {duplicate_count} duplicate records")
    st.info(f"Total records in database: {len(updated_db)}")

def handle_file_upload(uploaded_file):
    if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        st.subheader("Preview of uploaded file")
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        
        if st.button("Save to Database", type="primary"):
            handle_save_button_click(df, uploaded_file)
    else:
        st.error("Please upload a valid Excel file (.xlsx or .xls)")

def show_upload_tab():
    st.header("Upload Data")
    st.write("This is the upload data tab.")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        handle_file_upload(uploaded_file)
    else:
        st.info("Awaiting file upload...")


def show_chat_tab():
    st.header("Chat Assistant")
    st.write("This is the chat assistant tab.")

def main():
    st.title("Dashboard")

    tab1, tab2 = st.tabs([
        "Upload Data",
        "Chat Assistant"
    ])

    with tab1:
        show_upload_tab()

    with tab2:
        show_chat_tab()
        
if __name__ == "__main__":
    main()