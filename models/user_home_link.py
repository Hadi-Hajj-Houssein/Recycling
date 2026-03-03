from sqlalchemy import Column , String , Integer , Float, ForeignKey
from db_main import Base
# from models.user import User
# from models.home import Home
# from sqlalchemy.orm import relationship
# from sqlalchemy import ForeignKey

class User_Home(Base):
    __tablename__ = 'user_home_link'
    id = Column(Integer, primary_key=True)
    home_id = Column(Integer, ForeignKey('home.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)