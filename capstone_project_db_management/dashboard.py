import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Excel Upload Dashboard",
    page_icon="📊",
    layout="centered"
)

DB_FILE = "database.xlsx"

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

def main():
    st.title("📊 Excel Upload Dashboard")
    
    st.header("Upload Excel File")
    
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            
            st.subheader("Preview of uploaded data")
            st.dataframe(df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            
            if st.button("Save to Database", type="primary"):
                updated_db, new_count, duplicate_count = save_to_database(df, uploaded_file.name)
                if new_count > 0:
                    st.success(f"Successfully added {new_count} new records to database!")
                if duplicate_count > 0:
                    st.info(f"Skipped {duplicate_count} duplicate records")
                st.info(f"Total records in database: {len(updated_db)}")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    main()