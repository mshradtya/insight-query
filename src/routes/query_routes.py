from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from slowapi.util import get_remote_address
from slowapi.extension import Limiter as ExtensionLimiter
from services.query_service import handle_query, save_query_history, get_query_history
from dependencies.auth import get_current_user
from auth.schemas import QueryHistoryOut

router = APIRouter()
limiter = ExtensionLimiter(key_func=get_remote_address)


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
@limiter.limit("5/minute")
async def process_query(
    request: Request, query: QueryRequest, user_id: int = Depends(get_current_user)
):
    sql_query, result = await handle_query(query.question)
    await save_query_history(user_id, query.question, sql_query)
    return {"question": query.question, "data": result}


@router.get("/queries/history", response_model=list[QueryHistoryOut])
async def fetch_query_history(user_id: int = Depends(get_current_user)):
    rows = await get_query_history(user_id)
    return [dict(row) for row in rows]
