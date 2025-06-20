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