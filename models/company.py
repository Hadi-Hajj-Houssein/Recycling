from sqlalchemy import Column, String, Integer
from db_main import Base

class Company(Base):                   
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    company_name = Column(String(450), nullable=False)
    email = Column(String(300), unique=True, nullable=False)
    password = Column(String(256), nullable=False)