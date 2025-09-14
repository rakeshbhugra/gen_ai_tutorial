import asyncio
from retell import Retell
from dotenv import load_dotenv
import os

load_dotenv()

retell_client = Retell(
  api_key=os.getenv("RETELL_API_KEY")
)

from_number = '+13322448167'
to_number = '+919588078815'

async def make_call(name, amount_due):
    try:
        response = await retell_client.call.create_phone_call(
            from_number=from_number,
            to_number=to_number,
            retell_llm_dynamic_variables={
                "name": name,
                "amount": amount_due
            }
        )
        print(f"Call initiated: {response}")
    except Exception as e:
        print(f"Error making call: {e}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(make_call())