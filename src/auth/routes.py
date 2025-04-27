from fastapi import APIRouter, HTTPException
from auth.schemas import UserCreate, TokenResponse
from auth.services import create_user, authenticate_user
from auth.jwt import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse)
async def signup(user: UserCreate):
    user_id = await create_user(user.email, user.password)
    access_token = create_access_token(data={"user_id": user_id})
    return {"access_token": access_token}


@router.post("/login", response_model=TokenResponse)
async def login(user: UserCreate):
    db_user = await authenticate_user(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"user_id": db_user["id"]})
    return {"access_token": access_token}
