from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from .db_tools import list_tables, describe_table, execute_query

model_name = "gemini-2.0-flash-exp"

root_agent = SequentialAgent(
    name="fintech_advisory_team",
    description="Analyzes financial goals and provides comprehensive savings/investment recommendations",
    sub_agents=[

    ]
)
