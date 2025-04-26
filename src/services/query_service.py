from llm.query_llm import generate_sql_from_question


def handle_query(question: str) -> str:
    sql_query = generate_sql_from_question(question)
    return sql_query
