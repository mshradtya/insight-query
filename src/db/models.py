from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    MetaData,
)
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

queries = Table(
    "queries",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("question", Text, nullable=False),
    Column("generated_sql", Text, nullable=False),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
)
