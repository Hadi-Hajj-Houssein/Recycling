from sqlalchemy import Column , String , Integer , Float , ForeignKey
from sqlalchemy.orm import relationship
from db_main import Base
from models.user import User
# from models.user_home_link import User_Home
# from home import Home
# from models.home import Home
from models.user import User
class Recyclables(Base):
    __tablename__ = 'recyclables'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False , unique=True)
    organic = Column(Float, default=0.0)
    paper = Column(Float, default=0.0)
    plastic = Column(Float, default=0.0)
    glass = Column(Float, default=0.0)
    metal = Column(Float, default=0.0)

    user = relationship("User", back_populates="recyclables")