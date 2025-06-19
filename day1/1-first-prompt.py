from genai_client import client

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain AI Agent for kids"
)

print(response.text)
