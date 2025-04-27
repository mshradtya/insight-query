from llm.query_llm import generate_sql_from_question
from db.database import database
from utils.logger import logger
from fastapi import HTTPException
from db.schema_fetcher import get_database_schema
import re


async def handle_query(question: str) -> list:
    logger.info(f"Received question: {question}")

    sql_query = await generate_sql_from_question(question)
    logger.info(f"Generated SQL: {sql_query}")

    # Validation
    if not await is_valid_sql(sql_query):
        logger.error(f"Invalid SQL generated: {sql_query}")
        raise HTTPException(
            status_code=400,
            detail="Generated SQL is invalid. Please rephrase your question.",
        )

    try:
        rows = await database.fetch_all(query=sql_query)
    except Exception as e:
        logger.exception(f"Database query failed for SQL: {sql_query}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

    return [dict(row) for row in rows]


async def is_valid_sql(sql_query: str) -> bool:
    sql_query = sql_query.strip().lower()

    # Must start with select
    if not sql_query.startswith("select"):
        return False

    schema_info = await get_database_schema()
    valid_tables = [
        line.split("(")[0].strip().lower() for line in schema_info.splitlines()
    ]

    # Check if at least one valid table name exists anywhere in the SQL
    for table in valid_tables:
        if re.search(rf"\b{table}\b", sql_query):
            return True

    return False
