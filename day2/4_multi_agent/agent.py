import logging

from google.adk import Agent
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.adk.tools import exit_loop, google_search

model_name = "gemini-2.0-flash-exp"

# Tools

def append_to_state(
    tool_context: ToolContext, field: str, response: str
) -> dict[str, str]:
    """Append new output to an existing state key.

    Args:
        field (str): a field name to append to
        response (str): a string to append to the field

    Returns:
        dict[str, str]: {"status": "success"}
    """
    existing_state = tool_context.state.get(field, [])
    tool_context.state[field] = existing_state + [response]
    logging.info(f"[Added to {field}] {response}")
    return {"status": "success"}


# Financial Planning Agents

market_researcher = Agent(
    name="market_researcher",
    model=model_name,
    description="Researches current market conditions and investment options",
    instruction="""
    FINANCIAL_GOALS:
    {{ FINANCIAL_GOALS? }}

    INSTRUCTIONS:
    Use Google search to research current market conditions, interest rates, and investment options relevant to achieving the financial goals described in FINANCIAL_GOALS.
    Focus on:
    - Current savings account interest rates
    - Investment options (stocks, bonds, mutual funds, ETFs)
    - Inflation rates and economic outlook
    - Risk assessment for different investment vehicles
    
    Use the 'append_to_state' tool to add your research to the field 'MARKET_RESEARCH'.
    """,
    tools=[google_search, append_to_state],
)

budget_analyzer = Agent(
    name="budget_analyzer",
    model=model_name,
    description="Analyzes current financial situation and spending patterns",
    instruction="""
    FINANCIAL_GOALS:
    {{ FINANCIAL_GOALS? }}

    USER_PROFILE:
    {{ USER_PROFILE? }}

    INSTRUCTIONS:
    Analyze the user's current financial situation based on USER_PROFILE and provide insights on:
    - Monthly income vs expenses breakdown
    - Areas where spending can be optimized
    - Current savings rate and potential improvements
    - Debt analysis and payoff strategies if applicable
    
    Use the 'append_to_state' tool to add your analysis to the field 'BUDGET_ANALYSIS'.
    """,
    tools=[append_to_state],
)

risk_assessment_team = ParallelAgent(
    name="risk_assessment_team", sub_agents=[market_researcher, budget_analyzer]
)

plan_validator = Agent(
    name="plan_validator",
    model=model_name,
    description="Reviews and validates the financial plan for feasibility",
    instruction="""
    INSTRUCTIONS:
    Review the SAVINGS_PLAN and assess:
    - Is the timeline realistic given the current financial situation?
    - Are the savings targets achievable?
    - Does the plan account for emergency funds?
    - Are the investment recommendations appropriate for the risk tolerance?
    - Does the plan consider inflation and life changes?

    If the SAVINGS_PLAN is comprehensive and realistic, exit the planning loop with your 'exit_loop' tool.

    If significant improvements can be made, use the 'append_to_state' tool to add your feedback to the field 'PLAN_FEEDBACK'.
    Explain your decision and briefly summarize the feedback you have provided.

    SAVINGS_PLAN:
    {{ SAVINGS_PLAN? }}

    MARKET_RESEARCH:
    {{ MARKET_RESEARCH? }}

    BUDGET_ANALYSIS:
    {{ BUDGET_ANALYSIS? }}
    """,
    tools=[append_to_state, exit_loop],
)

financial_planner = Agent(
    name="financial_planner",
    model=model_name,
    description="Creates detailed savings plans based on financial goals and research",
    instruction="""
    INSTRUCTIONS:
    Your goal is to create a comprehensive savings plan based on the FINANCIAL_GOALS: {{ FINANCIAL_GOALS? }}
    
    - If there is PLAN_FEEDBACK, use those insights to improve the plan
    - If there is MARKET_RESEARCH, incorporate current market conditions into your recommendations
    - If there is BUDGET_ANALYSIS, use the spending insights to create realistic savings targets
    - If there is a SAVINGS_PLAN, improve and refine it based on new information
    - Use the 'append_to_state' tool to write your savings plan to the field 'SAVINGS_PLAN'
    - Include specific monthly savings amounts, investment allocations, and timeline milestones
    - Summarize what you focused on in this planning iteration

    SAVINGS_PLAN:
    {{ SAVINGS_PLAN? }}

    MARKET_RESEARCH:
    {{ MARKET_RESEARCH? }}

    BUDGET_ANALYSIS:
    {{ BUDGET_ANALYSIS? }}

    PLAN_FEEDBACK:
    {{ PLAN_FEEDBACK? }}
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
    tools=[append_to_state],
)

financial_researcher = Agent(
    name="financial_researcher",
    model=model_name,
    description="Research financial strategies and market data using Google search",
    instruction="""
    FINANCIAL_GOALS:
    {{ FINANCIAL_GOALS? }}
    
    SAVINGS_PLAN:
    {{ SAVINGS_PLAN? }}

    PLAN_FEEDBACK:
    {{ PLAN_FEEDBACK? }}

    INSTRUCTIONS:
    - If there is PLAN_FEEDBACK, research specific strategies to address those concerns
    - If there is a SAVINGS_PLAN, research additional strategies to optimize it
    - If these are empty, research general financial planning strategies for the goals in FINANCIAL_GOALS
    - Use your Google search tool to gather current information about:
        - Investment strategies and current market trends
        - Savings strategies and interest rates
        - Financial planning best practices
        - Economic factors affecting long-term savings
    - Use the 'append_to_state' tool to add your research to the field 'FINANCIAL_RESEARCH'
    - Summarize the key insights you've discovered
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
    tools=[google_search, append_to_state],
)

plan_summarizer = Agent(
    name="plan_summarizer",
    model=model_name,
    description="Summarizes all financial planning data into an easy-to-understand format for the user",
    instruction="""
    FINANCIAL_GOALS:
    {{ FINANCIAL_GOALS? }}

    USER_PROFILE:
    {{ USER_PROFILE? }}

    SAVINGS_PLAN:
    {{ SAVINGS_PLAN? }}

    MARKET_RESEARCH:
    {{ MARKET_RESEARCH? }}

    BUDGET_ANALYSIS:
    {{ BUDGET_ANALYSIS? }}

    FINANCIAL_RESEARCH:
    {{ FINANCIAL_RESEARCH? }}

    INSTRUCTIONS:
    Create a comprehensive, easy-to-understand summary of the financial plan that includes:
    
    1. **Executive Summary**: Brief overview of the user's goals and recommended approach
    2. **Your Financial Snapshot**: Current situation based on USER_PROFILE and BUDGET_ANALYSIS
    3. **The Plan**: Clear, actionable steps from SAVINGS_PLAN broken down by timeframe
    4. **Investment Strategy**: Simplified explanation of recommended investments from MARKET_RESEARCH
    5. **Key Insights**: Most important findings from FINANCIAL_RESEARCH
    6. **Next Steps**: Immediate actions the user should take
    7. **Milestones**: Key checkpoints and timeline
    
    Use simple language, avoid jargon, and make it actionable. Present numbers in an easy-to-scan format.
    Use the 'append_to_state' tool to save the summary to the field 'FINAL_SUMMARY'.
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
    tools=[append_to_state],
)

planning_workshop = LoopAgent(
    name="planning_workshop",
    description="Iterates through research and planning to create an optimal savings plan",
    sub_agents=[financial_researcher, financial_planner, plan_validator],
    max_iterations=3,
)

financial_advisory_team = SequentialAgent(
    name="financial_advisory_team",
    description="Create a comprehensive financial savings plan and save it as a document",
    sub_agents=[planning_workshop, risk_assessment_team, plan_summarizer],
)

root_agent = Agent(
    name="financial_advisor",
    model=model_name,
    description="Guides users in creating personalized financial savings plans",
    instruction="""
    - Welcome the user and explain that you'll help them create a comprehensive savings plan
    - Ask them to describe:
        1. Their primary financial goal (e.g., house down payment, retirement, emergency fund, vacation)
        2. Target amount needed
        3. Desired timeline
        4. Current monthly income and major expenses
        5. Risk tolerance (conservative, moderate, aggressive)
    - When they respond, use the 'append_to_state' tool to store their goals in 'FINANCIAL_GOALS' 
      and their personal info in 'USER_PROFILE', then transfer to the 'financial_advisory_team' agent
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
    tools=[append_to_state],
    sub_agents=[financial_advisory_team],
)
