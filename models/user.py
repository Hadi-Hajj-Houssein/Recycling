from sqlalchemy import Column , String , Integer , Float
from sqlalchemy.orm import relationship
from db_main import Base
# from user_home_link import User_Home
# from home import Home

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(300),unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    username = Column(String(450), nullable=False) 
    amount = Column(Float)
    #homes = relationship(Home, secondary=User_Home, back_populates="residents")

