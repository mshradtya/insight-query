from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.query_service import handle_query
from dependencies.api_key import verify_api_key

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query", dependencies=[Depends(verify_api_key)])
async def process_query(request: QueryRequest):
    result = await handle_query(request.question)
    return {"question": request.question, "data": result}
