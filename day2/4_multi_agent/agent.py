import logging
import uuid
from google.adk.agents import Agent, SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.adk.tools import exit_loop

model_name = "gemini-2.5-flash-preview-04-17"

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


def generate_uuid() -> str:
    """Generate a UUID."""
    return str(uuid.uuid4())


def write_json_file(
    tool_context: ToolContext, filename: str, data: str
) -> dict[str, str]:
    """Write data to a JSON file.
    
    Args:
        filename (str): The filename to write to (should include .json extension)
        data (str): JSON string data to write to file
        
    Returns:
        dict[str, str]: {"status": "success", "filename": filename} or {"status": "error", "message": error_message}
    """
    try:
        import json
        # Validate that data is valid JSON
        json.loads(data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
        
        logging.info(f"Successfully wrote file: {filename}")
        return {"status": "success", "filename": filename}
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON data: {str(e)}"
        logging.error(error_msg)
        return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"Error writing file {filename}: {str(e)}"
        logging.error(error_msg)
        return {"status": "error", "message": error_msg}


# Agents

financial_planner = Agent(
    name="financial_planner",
    model=model_name,
    description="Creates detailed financial savings plans based on user goals",
    instruction="""
    You are a financial planning expert. Based on the user's goals and profile:
    1. Create a comprehensive savings plan with specific recommendations
    2. Include timeline, monthly savings targets, and strategies
    3. Use the 'append_to_state' tool to store your plan in 'FINANCIAL_PLAN'
    4. Be specific and actionable in your recommendations
    
    When data is missing, make realistic assumptions based on common scenarios:
    - If age is missing, assume 30 years old
    - If income is missing, assume median income for their location ($60,000 annually)
    - If current savings is missing, assume $5,000
    - If timeline is missing, assume 3-5 years for most goals
    - If risk tolerance is missing, assume moderate risk tolerance
    - Always state your assumptions clearly in the plan
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,
    ),
    tools=[append_to_state],
)

plan_validator = Agent(
    name="plan_validator",
    model=model_name,
    description="Reviews and validates financial plans, providing feedback or approval",
    instruction="""
    You are a financial plan validator. Review the financial plan and:
    1. Check if the plan is realistic and achievable
    2. Verify that it addresses the user's goals
    3. If the plan needs improvement, provide specific feedback using 'append_to_state' to store in 'VALIDATION_FEEDBACK'
    4. If the plan is good, simply respond with "APPROVED" and use 'append_to_state' to store "APPROVED" in 'VALIDATION_STATUS'
    5. Always end your response with either "NEEDS_REVISION" or "APPROVED"
    
    When validating plans with missing or assumed data:
    - Validate that the assumptions made are reasonable and clearly stated
    - Check if the plan would work for typical scenarios with the assumed values
    - If critical information is missing that would significantly impact the plan, request clarification
    - Accept reasonable assumptions for common missing data (age, income, timeline, etc.)
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
    tools=[append_to_state, exit_loop],
)

planning_workshop = LoopAgent(
    name="planning_workshop",
    description="Iterates through research and planning to create an optimal savings plan",
    sub_agents=[financial_planner, plan_validator],
    max_iterations=3,
)

write_user_data = Agent(
    name="write_user_data",
    model=model_name,
    description="Writes user data and financial plan to a JSON file.",
    instruction="""
    You will create a comprehensive document containing the user's financial plan.
    1. Generate a unique file name using the 'generate_uuid' tool (add .json extension)
    2. Gather all data from the state (FINANCIAL_GOALS, USER_PROFILE, FINANCIAL_PLAN, etc.)
    3. Create a well-structured JSON document with all the information
    4. Use the 'write_json_file' tool to write the complete financial plan document
    5. If any required data is missing from state, make reasonable assumptions and note them in the document
    6. Include sections for: user profile, financial goals, savings plan, assumptions made, and recommendations
    
    Example JSON structure:
    {
        "document_id": "generated_uuid",
        "created_at": "current_timestamp",
        "user_profile": {...},
        "financial_goals": {...},
        "financial_plan": {...},
        "assumptions_made": [...],
        "recommendations": [...]
    }
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0,
    ),
    tools=[generate_uuid, write_json_file, append_to_state],
)

plan_summarizer = Agent(
    name="plan_summarizer",
    model=model_name,
    description="Summarizes the financial plan.",
    instruction="""
    You will be the final step of advisory team who response to user's goal.
    """,
)

financial_advisory_team = SequentialAgent(
    name="financial_advisory_team",
    description="Create a comprehensive financial savings plan and save it as a. Write user data is mandatory for the step",
    sub_agents=[planning_workshop, write_user_data, plan_summarizer],
)

root_agent = Agent(
    name="greeter",
    model=model_name,
    description="Guides users in creating personalized financial savings plans",
    instruction="""
    - Welcome the user and explain that you'll help them create a comprehensive savings plan
    - Ask them to describe:
        1. Their primary financial goal (e.g., house down payment, retirement, emergency fund, vacation)
        2. Target amount needed
        3. Optional: age, income, current savings, timeline, risk tolerance
    - When they respond, use the 'append_to_state' tool to store their goals in 'FINANCIAL_GOALS' 
      and their personal info in 'USER_PROFILE'
    - If they provide incomplete information, reassure them that realistic assumptions will be made for missing details
    - Once you have collected this information, the financial advisory team will take over to create their plan
    - Don't pressure users to provide every detail - work with what they give you
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,  # Greeter is friendly person. That's why need very variant response here
    ),
    tools=[append_to_state],
    sub_agents=[financial_advisory_team],
)
