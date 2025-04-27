import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()


async def verify_api_key(x_api_key: str = Header(...)):
    expected_api_key = os.getenv("INSIGHTQUERY_API_KEY")
    if x_api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
