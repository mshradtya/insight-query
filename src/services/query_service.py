from llm.query_llm import generate_sql_from_question


async def handle_query(question: str) -> str:
    sql_query = await generate_sql_from_question(question)
    return sql_query
