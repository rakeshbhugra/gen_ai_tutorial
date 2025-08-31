from langchain_community.utilities import SerpAPIWrapper

search = SerpAPIWrapper(serpapi_api_key="4f4e20ae4db0c405712f474d569913067eb217e2ed5b46653530b73dd05aa48a")

results = search.run("What is LangGraph?")
print(results)