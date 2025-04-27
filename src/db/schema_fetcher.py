from db.database import client_database


async def get_database_schema() -> str:
    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    rows = await client_database.fetch_all(query=query)

    schema = {}
    for row in rows:
        table = row["table_name"]
        column = row["column_name"]
        schema.setdefault(table, []).append(column)

    schema_str = ""
    for table, columns in schema.items():
        schema_str += f"{table}({', '.join(columns)})\n"

    return schema_str.strip()
