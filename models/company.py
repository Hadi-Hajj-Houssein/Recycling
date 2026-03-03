from sqlalchemy import Column , String , Integer , Float
from sqlalchemy.orm import relationship
from db_main import Base
# from models.user_home_link import User_Home
# from home import Home
# from models.home import Home

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    email = Column(String(300),unique=True, nullable=False)
    password = Column(String(256), nullable=False)

