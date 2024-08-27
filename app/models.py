from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, nullable=False),
    Column("hashed_password", String(100), nullable=False),
)