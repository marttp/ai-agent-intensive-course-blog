from google.genai import types
from genai_client import client

short_config = types.GenerateContentConfig(max_output_tokens=100)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=short_config,
    contents="Write an essay about the world after smartphone.",
)

print(response.text)
