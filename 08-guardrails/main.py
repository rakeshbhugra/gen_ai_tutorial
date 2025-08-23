# This is what happens when you use OpenAI moderation
import openai
from dotenv import load_dotenv
load_dotenv()

# OpenAI's moderation model (separate from GPT)
moderation_response = openai.Moderation.create(
    input="Your text here"
)

print(moderation_response)