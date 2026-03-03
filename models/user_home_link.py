from sqlalchemy import Column , String , Integer , Float
from db_main import Base
from user import User
from sqlalchemy.orm import relationship
from sqlalchemy import ForeinKey
from home import Home 

class Home(Base):
    __tablename__ = 'user_home_link'
    id = Column(Integer, primary_key=True)
    home_id = Column(Integer, ForeinKey('Home.id'), nullable=False)
    user_id = Column(Integer, ForeinKey('User.id'), nullable=False)