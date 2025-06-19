from google.genai import types
from genai_client import client

import enum


class FraudStatus(enum.Enum):
    FRAUD = "fraud"
    LEGITIMATE = "legitimate"


zero_shot_prompt = """Classify messages as FRAUD or LEGITIMATE.
Message: "Congratulations! You've won $10,000! Click this link immediately 
to claim your prize before it expires in 24 hours. 
Act now: http://amaz0n.com/claim-prize"
Classification: """

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        response_mime_type="text/x.enum", response_schema=FraudStatus
    ),
    contents=zero_shot_prompt,
)

print(response.text)
