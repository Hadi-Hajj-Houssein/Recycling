from sqlalchemy import Column , String , Integer , Float 
from db_main import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(300),unique=True, nullable=False)
    password = Column(String(256),nullable=False)
    # __table_args_ = {
    #     CheckConstraint = ("length(password)>=8",name = "password_min_length"),
    # } manne met2akkad 100% bedde chouf kif 
    #money = 
