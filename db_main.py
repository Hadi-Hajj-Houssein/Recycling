from sqlalchemy import create_engine # khbar db 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_NeuHZUlzFd43@ep-little-silence-amsr4urz-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Base = declarative_base()