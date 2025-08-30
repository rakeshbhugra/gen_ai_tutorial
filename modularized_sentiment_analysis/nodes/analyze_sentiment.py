from litellm import completion
import json
from modularized_sentiment_analysis.state import State
from pydantic import BaseModel
from typing import Literal

class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]

def analyze_sentiment(state: State):
    print("Analyzing sentiment...")

    response = completion(
        model="openai/gpt-4.1-mini",
        messages=state.messages,
        response_format=SentimentResponse
    )

    json_content = response.choices[0].message.content
    json_dict = json.loads(json_content)
    sentiment_respone = SentimentResponse(**json_dict)

    state.sentiment = sentiment_respone.sentiment

    return state