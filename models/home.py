from sqlalchemy import Column , String , Integer , Float
from db_main import Base
from user import User
from sqlalchemy.orm import relationship
class Home(Base):
    __tablename___ = 'home'
    id = Column(Integer, primary_key=True)
    address = Column(String(300), nullable=False)

    residents = relationship("User", secondary="User_Home", back_populates="homes")