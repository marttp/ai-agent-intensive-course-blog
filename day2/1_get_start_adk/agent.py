from google.adk.agents import Agent

root_agent = Agent(
    name="noob_agent",
    model="gemini-2.0-flash",
    description=("Simple agent without any tools"),
    instruction=("You are a helpful agent who can answer user questions."),
)
