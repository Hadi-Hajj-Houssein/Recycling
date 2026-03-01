# hay la ma kel marra a3mil base = declarative base 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker
db_URL = "postgresql+psycopg2://postgres:123@localhost:5432/Recycling"

engine = create_engine(db_URL, pool_pre_ping=True)
session  = sessionmaker(bind = engine, autocommit = False)
SessionLocal =sessionmaker(
    autocommit =False,
    autoflush =False,
    bind =engine
)
Base = declarative_base()
