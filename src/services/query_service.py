from llm.query_llm import generate_sql_from_question
from db.database import client_database, system_database
from utils.logger import logger
from fastapi import HTTPException
from db.schema_fetcher import get_database_schema
import re
from db.models import queries
import datetime


async def handle_query(question: str) -> tuple[str, list[dict]]:
    logger.info(f"Received question: {question}")

    sql_query = await generate_sql_from_question(question)
    logger.info(f"Generated SQL: {sql_query}")

    if not await is_valid_sql(sql_query):
        logger.error(f"Invalid SQL generated: {sql_query}")
        raise HTTPException(
            status_code=400,
            detail="Generated SQL is invalid. Please rephrase your question.",
        )

    try:
        rows = await client_database.fetch_all(query=sql_query)
    except Exception as e:
        logger.exception(f"Database query failed for SQL: {sql_query}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

    return sql_query, [dict(row) for row in rows]


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


async def save_query_history(user_id: int, question: str, generated_sql: str):
    query = queries.insert().values(
        user_id=user_id,
        question=question,
        generated_sql=generated_sql,
        created_at=datetime.datetime.utcnow(),
    )
    await system_database.execute(query)


async def get_query_history(user_id: int):
    query = (
        queries.select()
        .where(queries.c.user_id == user_id)
        .order_by(queries.c.created_at.desc())
        .limit(20)  # last 20 queries
    )
    return await system_database.fetch_all(query)
