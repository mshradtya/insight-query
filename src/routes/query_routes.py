from fastapi import APIRouter
from pydantic import BaseModel
from services.query_service import handle_query

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
async def process_query(request: QueryRequest):
    result = await handle_query(request.question)
    return {"question": request.question, "data": result}
