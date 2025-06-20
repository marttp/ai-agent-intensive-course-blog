from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from .db_tools import list_tables, describe_table, execute_query

model_name = "gemini-2.0-flash-exp"

financial_goal_analyzer = Agent(
    name="financial_goal_analyzer",
    model=model_name,
    description="Analyzes financial goals and determines feasibility and timeline",
    instruction="""
    FINANCIAL_REQUEST:
    {{ FINANCIAL_REQUEST? }}

    INSTRUCTIONS:
    Analyze the financial goal described in FINANCIAL_REQUEST. Consider:
    - Goal amount and timeline
    - Monthly savings capacity based on income/expenses
    - Risk tolerance and investment horizon
    - Feasibility assessment
    - Recommended monthly contribution amounts
    
    Provide a detailed analysis report including achievability score (1-10) and key recommendations.
    """,
    output_key="goal_analysis_report",
)

savings_options_agent = Agent(
    name="savings_options_agent",
    model=model_name,
    description="Recommends appropriate financial products and savings strategies",
    instruction="""
    FINANCIAL_REQUEST:
    {{ FINANCIAL_REQUEST? }}
    
    GOAL_ANALYSIS:
    {{ goal_analysis_report? }}

    INSTRUCTIONS:
    Based on the financial goal and analysis, recommend the best savings/investment options:
    - High-yield savings accounts for short-term goals
    - CDs for medium-term goals with guaranteed returns
    - Investment accounts (stocks, bonds, ETFs) for long-term growth
    - Virtual credit cards with cashback rewards
    - Personal loans if additional funding is needed
    - Automated savings programs and apps
    
    Provide specific product recommendations with pros/cons and expected returns.
    """,
    output_key="savings_options_report",
)

user_record_agent = Agent(
    name="user_record_agent",
    model=model_name,
    description="Stores and manages user financial profiles and history",
    instruction="""
    FINANCIAL_REQUEST:
    {{ FINANCIAL_REQUEST? }}
    
    GOAL_ANALYSIS:
    {{ goal_analysis_report? }}
    
    SAVINGS_OPTIONS:
    {{ savings_options_report? }}
    
    FINANCIAL_ROADMAP:
    {{ financial_roadmap? }}

    INSTRUCTIONS:
    Store the user's financial profile and session data in the database. Include:
    - User identification (generate unique ID if new user)
    - Financial goals and target amounts
    - Risk tolerance and timeline preferences
    - Recommended savings/investment strategies
    - Progress tracking milestones
    - Session timestamp and interaction history
    
    Use the available database tools to:
    1. Check if user exists in database
    2. Create or update user profile record
    3. Store the current financial consultation session
    4. Return confirmation of successful storage with user ID
    """,
    output_key="user_record_status",
    tools=[list_tables, describe_table, execute_query],
)

fintech_coordinator = ParallelAgent(
    name="fintech_coordinator",
    sub_agents=[financial_goal_analyzer, savings_options_agent],
)

reward_breakdown_agent = Agent(
    name="reward_breakdown_agent",
    model=model_name,
    description="Creates comprehensive financial plan with reward breakdown",
    instruction="""
    FINANCIAL_REQUEST:
    {{ FINANCIAL_REQUEST? }}
    
    GOAL_ANALYSIS:
    {{ goal_analysis_report? }}
    
    SAVINGS_OPTIONS:
    {{ savings_options_report? }}

    INSTRUCTIONS:
    Create a comprehensive financial plan that combines the goal analysis and savings options:
    - Break down the reward system based on milestones
    - Create actionable monthly/quarterly steps
    - Suggest automation strategies
    - Provide tracking metrics and success indicators
    - Include contingency plans for market volatility
    
    Present as a structured financial roadmap with clear next steps.
    """,
    output_key="financial_roadmap",
)

root_agent = SequentialAgent(
    name="fintech_advisory_team",
    description="Analyzes financial goals and provides comprehensive savings/investment recommendations",
    sub_agents=[
        fintech_coordinator,
        reward_breakdown_agent,
        user_record_agent,
    ]
)
