from sqlalchemy import Column , String , Integer , Float
from db_main import Base
from user import User
from home import Home
from sqlalchemy.orm import relationship
from sqlalchemy import ForeinKey

class User_Home(Base):
    __tablename__ = 'user_home_link'
    id = Column(Integer, primary_key=True)
    home_id = Column(Integer, ForeinKey('home.id'), nullable=False)
    user_id = Column(Integer, ForeinKey('user.id'), nullable=False)