from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
import datetime

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
)
