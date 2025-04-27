from llm.query_llm import generate_sql_from_question


async def handle_query(question: str) -> str:
    sql_query = await generate_sql_from_question(question)

    # basic Validation
    if not is_valid_sql(sql_query):
        raise ValueError("Generated SQL is invalid. Please rephrase your question.")

    return sql_query


def is_valid_sql(sql_query: str) -> bool:
    sql_query = sql_query.strip().lower()
    # ensure it starts with select and mentions 'employees'
    return sql_query.startswith("select") and "from employees" in sql_query
