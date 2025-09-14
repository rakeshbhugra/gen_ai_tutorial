import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI LLM
llm = OpenAI(api_token=os.getenv("OPENAI_API_KEY"))

# Create sample data
sales_data = {
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "sales": [5000, 3200, 2900, 4100, 2300, 2100, 2500, 2600, 4500, 7000],
    "profit": [1500, 1200, 800, 1600, 700, 600, 900, 950, 1800, 2800],
    "region": ["North America", "Europe", "Europe", "Europe", "Europe", "Europe", "North America", "Oceania", "Asia", "Asia"]
}

# Create regular pandas DataFrame first
regular_df = pd.DataFrame(sales_data)

# Convert to SmartDataframe (new PandasAI API)
df = SmartDataframe(regular_df, config={"llm": llm})

# Basic queries - just ask in natural language!
print("=== Basic PandasAI Queries ===\n")

# Query 1: Simple filtering
print("1. Top 5 countries by sales:")
result1 = df.chat("Which are the top 5 countries by sales?")
print(result1)
print("\n" + "="*50 + "\n")

# Query 2: Aggregation
print("2. Total sales by region:")
result2 = df.chat("What is the total sales by region?")
print(result2)
print("\n" + "="*50 + "\n")

# Query 3: Calculations
print("3. Countries with profit margin > 30%:")
result3 = df.chat("Show me countries where profit margin is greater than 30%")
print(result3)
print("\n" + "="*50 + "\n")

# Query 4: Statistical analysis
print("4. Average sales and profit:")
result4 = df.chat("What are the average sales and profit?")
print(result4)
print("\n" + "="*50 + "\n")

# Query 5: More complex analysis
print("5. Best performing country by profit margin:")
result5 = df.chat("Which country has the highest profit margin percentage?")
print(result5)
print("\n" + "="*50 + "\n")

# Working with another DataFrame
print("=== Additional Analysis ===\n")

# Query 6: Create summary with profit margins
print("6. Summary with profit margins:")
result6 = df.chat("Create a summary showing country, sales, and profit margin percentage")
print(result6)
print("\n" + "="*50 + "\n")

# Query 7: Statistical description
print("7. Statistical summary:")
summary = df.chat("Provide a statistical summary of the sales and profit columns")
print(summary)