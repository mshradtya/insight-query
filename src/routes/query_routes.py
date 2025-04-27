from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from slowapi.util import get_remote_address
from slowapi.extension import Limiter as ExtensionLimiter
from services.query_service import handle_query
from dependencies.api_key import verify_api_key

router = APIRouter()
limiter = ExtensionLimiter(key_func=get_remote_address)


class QueryRequest(BaseModel):
    question: str


@router.post("/query", dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")  # 5 requests per minute allowed
async def process_query(request: Request, query: QueryRequest):
    result = await handle_query(query.question)
    return {"question": query.question, "data": result}
