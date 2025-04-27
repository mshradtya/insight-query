from fastapi import FastAPI
from contextlib import asynccontextmanager
import auth.routes
from db.database import system_database, client_database
from routes import query_routes
from slowapi import Limiter
from slowapi.util import get_remote_address
import auth

# rate limiter setup
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    await system_database.connect()
    print("system db connected")
    await client_database.connect()
    print("client db connected")

    # ⚡ Manually create users table
    create_users_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    await system_database.execute(create_users_table_sql)

    yield
    # shutdown logic
    await system_database.disconnect()
    await client_database.disconnect()


app = FastAPI(lifespan=lifespan)

# init limiter middleware
app.state.limiter = limiter

from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.requests import Request


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please slow down."},
    )


# Register your routes
app.include_router(auth.routes.router)
app.include_router(query_routes.router, prefix="/api")
