from sqlalchemy import Column, String, Integer
from db_main import Base
from sqlalchemy.orm import relationship

class Home(Base):
    __tablename__ = 'home'
    id = Column(Integer, primary_key=True)
    address = Column(String(300), nullable=False)
    residents = relationship("models.user.User", secondary="user_home_link", back_populates="homes")