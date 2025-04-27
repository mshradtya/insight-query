from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import database
from routes import query_routes
from slowapi import Limiter
from slowapi.util import get_remote_address

# rate limiter setup
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    await database.connect()
    print("db connected")
    yield
    # shutdown logic
    await database.disconnect()


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
app.include_router(query_routes.router, prefix="/api")
