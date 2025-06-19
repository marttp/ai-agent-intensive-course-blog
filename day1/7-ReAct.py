from genai_client import client
from google.genai import types

model_instructions = """
Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation,
Observation is understanding relevant information from an Action's output and Action can be one of three types:
 (1) <search>entity</search>, which searches the exact entity on documents and returns the first paragraph if it exists. If not, it
     will return some similar entities to search and you can try to search the information from those topics.
 (2) <lookup>keyword</lookup>, which returns the next sentence containing keyword in the current context. This only does exact matches,
     so keep your searches short.
 (3) <finish>answer</finish>, which returns the answer and finishes the task.
"""

example1 = """Question
What database does Netflix use for its recommendation engine?

Thought 1
I need to find information about Netflix's recommendation engine and what database technology they use for it.

Action 1
<search>Netflix recommendation engine</search>

Observation 1
Netflix uses a sophisticated recommendation system that analyzes user behavior and preferences to suggest content.

Thought 2
This gives me general information but doesn't specify the database. Let me search more specifically for Netflix's database architecture.

Action 2
<lookup>database</lookup>

Observation 2
Netflix uses Apache Cassandra as their primary database for the recommendation engine due to its ability to handle massive amounts of data and provide low-latency reads.

Thought 3
Based on the information found, Netflix uses Apache Cassandra for their recommendation engine database.

Action 3
<finish>Apache Cassandra</finish>
"""

question = """Question
What load balancing algorithm does AWS Application Load Balancer use by default?
"""

# You will perform the Action; so generate up to, but not including, the Observation.
react_config = types.GenerateContentConfig(
    stop_sequences=["\nObservation"],
    system_instruction=model_instructions + example1,
)

# Create a chat that has the model instructions and examples pre-seeded.
react_chat = client.chats.create(
    model="gemini-2.0-flash",
    config=react_config,
)

resp = react_chat.send_message(question)
print(resp.text)
