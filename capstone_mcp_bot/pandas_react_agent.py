import subprocess
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def execute_python_code(code: str) -> str:
    """Execute the given Python code and return the output or error message.
    
    Parameters
    ----------
    code : str
        This should only be python code. Nothing else

    Returns
    -------
    str
        The output from the executed code or an error message    
    
    """
    try:
        # print("generated code:\n", code)
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

agent = create_react_agent(
    model="openai:gpt-4.1-mini",
    tools=[execute_python_code],
    prompt="""
You are a data analyst. Use the tool to execute python code to answer user questions.
You only have to work on this file:
'capstone_project_db_management/database.xlsx'

The schema looks like this"
Index(['Customer ID', 'Customer Name', 'Email', 'Phone', 'Service Type',
       'Amount Due', 'Due Date', 'User Status', 'Last Contact',
       'Payment Status', 'Follow Up Required'],
      dtype='object')


for example, if the user asks you to read the excel file and show the first 5 rows,
you should respond with the following python code:
```python
import pandas as pd
df = pd.read_excel('capstone_project_db_management/database.xlsx')
print(df.head())
```

If you write code incorrectly, you will get an error message back. Use that to correct your code and try again.

"""
)

def pandas_agent(query: str) -> str:
    """Give natural language query on the excel file and get the response
    
    Parameters
    ----------
    query : str
        The natural language query to execute on the Excel file.
    
    Returns
    -------
    str
        The response from the agent after executing the query.
    """

    user_query = query
    result = agent.invoke({"messages": [("user", user_query)]})
    # print("Agent response:")
    # for message in result["messages"]:
    #     print(f"{message.type}: {message.content}")

    final_response = result["messages"][-1].content

    return final_response

if __name__ == "__main__":
    query = "find me list of all the customer who have user status as  followed_up"
    response = pandas_agent(query)
    print("Response from agent:")
    print(response)