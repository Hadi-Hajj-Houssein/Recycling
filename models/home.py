from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db_main import Base

class Home(Base):
    __tablename__ = 'home'
    id = Column(Integer, primary_key=True)
    address = Column(String(300), nullable=False)
    residents = relationship("User", secondary="user_home_link", back_populates="homes")