from genai_client import client

chat = client.chats.create(model="gemini-2.0-flash", history=[])

# 1 - Introduce myself
response = chat.send_message("Hello! My name is Mart.")
print(response.text)

# 2 - Instead of one shot message, use chat to have conversation
response = chat.send_message("Can you tell me something interesting about deep sea?")
print(response.text)

# 3 - Since we have history, ask if it remember you
response = chat.send_message('Do you remember what my name is?')
print(response.text)