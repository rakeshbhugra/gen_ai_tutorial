from mcp.server.fastmcp import FastMCP
from pandas_react_agent import pandas_agent

mcp = FastMCP("MCP Bot Server")

@mcp.tool()
def analytics_team(query: str) -> str:
    """Query the Excel file using natural language
    
    Parameters
    ----------
    query : str
        The natural language query to execute on the Excel file.
    
    Returns
    -------
    str
        The response from the agent after executing the query.
    """
    return pandas_agent(query)


@mcp.tool()
def email_team(to: str, subject: str, body: str) -> str:
    """Send an email (simulated)
    
    Parameters
    ----------
    to : str
        The recipient's email address.
    subject : str
        The subject of the email.
    body : str
        The body content of the email.
    
    Returns
    -------
    str
        Confirmation message that the email was "sent".
    """
    # Simulate sending an email by printing to console
    print(f"Sending email to: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    to = "rakeshkbhugra@gmail.com"
    return f"Email sent to {to} with subject '{subject}'."

# Run server with streamable_http transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
