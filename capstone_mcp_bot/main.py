from pandasai import SmartDataframe
import pandas as pd
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize OpenAI LLM
llm = OpenAI(api_token=os.getenv("OPENAI_API_KEY"))

file_path = "capstone_project_db_management/database.xlsx"
df = pd.read_excel(file_path)

df = SmartDataframe(df, config={"llm": llm})

response = df.chat("who has the highest amount due?")
print(response)