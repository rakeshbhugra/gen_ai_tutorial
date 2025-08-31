from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
load_dotenv()

search = SerpAPIWrapper()

result = search.run("What is today's news on Nvidia?")

print(result)