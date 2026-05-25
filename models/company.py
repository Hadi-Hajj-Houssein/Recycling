from sqlalchemy import Column, String, Integer
from db_main import Base
from sqlalchemy.orm import relationship 
class Company(Base):                   
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    company_name = Column(String(450), nullable=False)
    email = Column(String(300), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    assigned_items = relationship("Recyclable_Item", back_populates="company")
    requests = relationship(
        "Request",
        back_populates="company"
    )