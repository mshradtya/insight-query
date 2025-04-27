from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import database
from routes import query_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    await database.connect()
    print("db connected")
    yield
    # shutdown logic
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

# Register your routes
app.include_router(query_routes.router, prefix="/api")
