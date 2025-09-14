import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI LLM
llm = OpenAI(api_token=os.getenv("OPENAI_API_KEY"))

# Load the actual database
print("Loading database.xlsx...")
df_raw = pd.read_excel("capstone_project_db_management/database.xlsx")

# Display basic info about the database
print(f"\nDatabase loaded successfully!")
print(f"Shape: {df_raw.shape}")
print(f"Columns: {df_raw.columns.tolist()}\n")

# Convert to SmartDataframe
df = SmartDataframe(df_raw, config={"llm": llm})

print("=== PandasAI Analysis of Customer Database ===\n")

# Query 1: Overview of the data
print("1. Database overview:")
result1 = df.chat("Provide a brief overview of this customer database including total records and key fields")
print(result1)
print("\n" + "="*50 + "\n")

# # Query 2: Payment status distribution
# print("2. Payment status distribution:")
# result2 = df.chat("What is the distribution of payment statuses in the database?")
# print(result2)
# print("\n" + "="*50 + "\n")

# # Query 3: Service types
# print("3. Service type breakdown:")
# result3 = df.chat("Show the count of customers by service type")
# print(result3)
# print("\n" + "="*50 + "\n")

# # Query 4: Amount due analysis
# print("4. Amount due analysis:")
# result4 = df.chat("What is the total, average, min and max amount due across all customers?")
# print(result4)
# print("\n" + "="*50 + "\n")

# # Query 5: Follow up required
# print("5. Follow-up required customers:")
# result5 = df.chat("How many customers require follow up? Show the count and percentage")
# print(result5)
# print("\n" + "="*50 + "\n")

# # Query 6: User status distribution
# print("6. User status distribution:")
# result6 = df.chat("What are the different user statuses and their counts?")
# print(result6)
# print("\n" + "="*50 + "\n")

# # Query 7: Overdue analysis
# print("7. Overdue payments:")
# result7 = df.chat("How many customers have overdue payments based on the due date?")
# print(result7)
# print("\n" + "="*50 + "\n")

# # Query 8: Top customers by amount due
# print("8. Top 5 customers by amount due:")
# result8 = df.chat("Show the top 5 customers with highest amount due including their name, amount, and payment status")
# print(result8)
# print("\n" + "="*50 + "\n")

# # Query 9: Service type revenue potential
# print("9. Revenue by service type:")
# result9 = df.chat("What is the total amount due grouped by service type?")
# print(result9)
# print("\n" + "="*50 + "\n")

# # Query 10: Customer contact analysis
# print("10. Recent contacts:")
# result10 = df.chat("Show customers who were last contacted more than 7 days ago and still have pending payments")
# print(result10)

# print("\n✅ Analysis complete!")