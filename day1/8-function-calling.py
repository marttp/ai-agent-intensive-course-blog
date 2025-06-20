from genai_client import client
from google.genai import types
import sqlite3

db_file = "sample.db"
db_conn = sqlite3.connect(db_file)


def list_tables() -> list[str]:
    """Retrieve the names of all tables in the database."""
    print(" - DB CALL: list_tables()")
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [t[0] for t in tables]


def describe_table(table_name: str) -> list[tuple[str, str]]:
    """Look up the table schema.

    Returns:
      List of columns, where each entry is a tuple of (column, type).
    """
    print(f" - DB CALL: describe_table({table_name})")
    cursor = db_conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()
    return [(col[1], col[2]) for col in schema]


def execute_query(sql: str) -> list[list[str]]:
    """Execute an SQL statement, returning the results."""
    print(f" - DB CALL: execute_query({sql})")

    cursor = db_conn.cursor()

    cursor.execute(sql)
    return cursor.fetchall()


# These are the Python functions defined above.
db_tools = [list_tables, describe_table, execute_query]

instruction = """You are a helpful chatbot that can interact with an SQL database
for a FinTech company managing credit card transactions. You will take the users questions and turn them into SQL
queries using the tools available. Once you have the information you need, you will
answer the user's question using the data returned.

Use list_tables to see what tables are present,
describe_table to understand the schema,
and execute_query to issue an SQL SELECT query."""

# Start a chat with automatic function calling enabled.
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction=instruction,
        tools=db_tools,
    ),
)

response = chat.send_message("Analyze the total transaction amount by card type?")
print(response.text)
