# from pydantic import BaseModel
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

########################################
####### Manual Parsing Approach ########
########################################

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
    model="openai/gpt-5-mini",
    messages=conversation_history,
)

raw_response = response['choices'][0]['message']['content']
# print("Raw AI Response:", raw_response)

# parse the response into the Email model
to_email = raw_response.split("To:")[1].split("Subject:")[0].strip()
subject = raw_response.split("Subject:")[1].split("Body:")[0].strip()
body = raw_response.split("Body:")[1].strip()

print(f"To: {to_email}\nSubject: {subject}\nBody: {body}s")

# How we will use it
# send_email(
#     to=to_email,
#     subject=subject,
#     body=body
# )


########################################
########################################


########################################
####### Pydantic Parsing Approach ######
########################################

from pydantic import BaseModel, ValidationError, Field, EmailStr
import json

class Email(BaseModel):
    To: EmailStr = Field(..., description="Recipient email address")
    Subject: str = Field(..., description="Subject of the email")
    Body: str = Field(..., description="Body content of the email")

conversation_history = [
    {"role": "system", "content": "You are an expert email writer. My name is John Doe. My manager's"},
]

user_input = """
Write an email to my manager about being late to work because of traffic.
email of my manager is: manager@example.com
name of my manager is: Jane Smith
"""

response = completion(
    model="openai/gpt-5-mini",
    messages=conversation_history,
    response_format=Email  # Specify the Pydantic model for structured response
)

json_content = response['choices'][0]['message']['content']

# load the json in pydantic object
parsed_data = json.loads(json_content)
try:
    email = Email(**parsed_data)
except ValidationError as e:
    print("Validation Error:", e)
    email = None

if email:
    print(email.To)
    print(email.Subject)
    print(email.Body)

else:
    print("Failed to parse email.")