import os; os.environ['LITELLM_LOG'] = 'CRITICAL'

from pydantic import BaseModel
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

class Email(BaseModel):
    To: str
    Subject: str
    Body: str

conversation_history = [
    {"role": "system", "content": "You are an expert email writer. My name is John Doe. My manager's"},
]

user_input = """
Write an email to my manager about being late to work because of traffic.
email of my manager is: manager@example.com
name of my manager is: Jane Smith

give me output in this format:
To:
Subject:
Body:
"""

conversation_history.append({"role": "user", "content": user_input})

response = completion(
    model="gemini/gemini-1.5-flash",
    messages=conversation_history,
)

raw_response = response['choices'][0]['message']['content']
print("Raw AI Response:", raw_response)

# parse the response into the Email model
to_email = raw_response.split("To:")[1].split("Subject:")[0].strip()
subject = raw_response.split("Subject:")[1].split("Body:")[0].strip()
body = raw_response.split("Body:")[1].strip()

print(f"To: {to_email}\nSubject: {subject}\nBody: {body}s")

# send_email(
#     to=to_email,
#     subject=subject,
#     body=body
# )