from fastapi import FastAPI
from routes import query_routes

app = FastAPI()

app.include_router(query_routes.router, prefix="/api")
