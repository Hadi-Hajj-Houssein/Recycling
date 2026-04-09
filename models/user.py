from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from db_main import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(300), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    username = Column(String(450), nullable=False)
    first_name = Column(String(450), nullable=False)
    last_name = Column(String(450), nullable=False)
    
    amount = Column(Float, nullable=False, default=0.0)
    recyclables      = relationship("Recyclables", back_populates="user", uselist=False) 
    recyclable_items = relationship("Recyclable_Item", back_populates="user")   
    total_recycled = relationship("UserTotalRecycled", back_populates="user", uselist=False)