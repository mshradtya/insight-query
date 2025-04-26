def generate_sql_from_question(question: str) -> str:
    # TEMP: Mock response. Later this will use LangChain.
    return f"SELECT * FROM employees WHERE city = 'Delhi';"
