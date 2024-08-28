from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from app.database import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, nullable=False),
    Column("hashed_password", String(100), nullable=False),
)

cryptocurrencies = Table(
    "cryptocurrencies",                                  
    metadata,                                            
    Column("id", Integer, primary_key=True),             
    Column("name", String),                              
    Column("symbol", String),                          
    Column("user_id", Integer, ForeignKey("users.id")),  
)