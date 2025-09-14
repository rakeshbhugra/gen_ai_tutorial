import subprocess
from litellm import completion

messages = [
    {"role": "user", "content": "Write a pandas script to print head of this file path: capstone_project_db_management/sample_upload.xlsx, Just write python code and nothing else"},
]

result = completion(
    model="gpt-4.1-mini",
    messages=messages,
)

code = result.choices[0].message.content
print("LLM Reponse:\n", code)
code = code.split("```python")
code = code[-1].rstrip('````')
print("Generated code:\n", code)

result = subprocess.run(['python'], input=code, capture_output=True, text=True)
print(result.stdout)