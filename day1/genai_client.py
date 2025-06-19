from google import genai
from google.api_core import retry
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helper.get_env import GEMINI_API_KEY

is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

genai.models.Models.generate_content = retry.Retry(predicate=is_retriable)(
    genai.models.Models.generate_content
)

client = genai.Client(api_key=GEMINI_API_KEY)
