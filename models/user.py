<<<<<<< HEAD
from sqlalchemy import Column , String , Integer , Float
from sqlalchemy.orm import relationship
=======
from sqlalchemy import Column , String , Integer , Float ,CheckConstraint
>>>>>>> ecd9845a080602ad4b34a9f85fcb754409ad4d9a
from db_main import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(300),unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    
    # Fixed spelling
    amount = Column(Float)

    homes = relationship("Home", secondary="user_home_link", back_populates="residents")
