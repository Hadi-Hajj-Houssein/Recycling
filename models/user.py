from sqlalchemy import Column , String , Integer , Float
from sqlalchemy.orm import relationship
from db_main import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(300), nullable=False)
    password = Column(String(256), nullable=False)
    username = Column(String(450),nullable= False , unique=True)
    amount = Column(Float)

    homes = relationship("Home", secondary="user_home_link", back_populates="residents")
