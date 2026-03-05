from sqlalchemy import Column , String , Integer , Float
from sqlalchemy.orm import relationship
from db_main import Base
# from models.user_home_link import User_Home
# from home import Home
# from models.home import Home

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(300),unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    company_name = Column(String(450), nullable=False) 
    amount = Column(Float)
    homes = relationship("models.home.Home", secondary="user_home_link", back_populates="residents")
    recyclables = relationship("Recyclables", uselist=False, back_populates="user")

