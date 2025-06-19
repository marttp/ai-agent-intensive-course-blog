from google.genai import types
from genai_client import client

# 1 - Simple prompt
prompt = """When I was 4 years old, my partner was 3 times my age. Now, I
am 20 years old. How old is my partner? Return the answer directly."""

response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

print(response.text)

# 2 - Chain of thought prompt
cot_prompt = """When I was 4 years old, my partner was 3 times my age. Now,
I am 20 years old. How old is my partner? Let's think step by step."""

cot_response = client.models.generate_content(
    model="gemini-2.0-flash", contents=cot_prompt
)

print(cot_response.text)
