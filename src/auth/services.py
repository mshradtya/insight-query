from db.database import system_database
from db.models import users
from passlib.context import CryptContext
from sqlalchemy import select
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(email: str, password: str):
    hashed_password = pwd_context.hash(password)
    query = users.insert().values(
        email=email,
        hashed_password=hashed_password,
        created_at=datetime.datetime.utcnow(),
    )
    user_id = await system_database.execute(query)
    return user_id


async def authenticate_user(email: str, password: str):
    query = select(users).where(users.c.email == email)
    user = await system_database.fetch_one(query)
    if not user:
        return None
    if not pwd_context.verify(password, user["hashed_password"]):
        return None
    return user
