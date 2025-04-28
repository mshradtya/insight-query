from pydantic import BaseModel, EmailStr
import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class QueryHistoryOut(BaseModel):
    id: int
    question: str
    generated_sql: str
    created_at: datetime.datetime
