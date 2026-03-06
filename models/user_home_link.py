from sqlalchemy import Column, Integer, ForeignKey
from db_main import Base

class User_Home(Base):
    __tablename__ = 'user_home_link'
    id = Column(Integer, primary_key=True)
    home_id = Column(Integer, ForeignKey('home.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)