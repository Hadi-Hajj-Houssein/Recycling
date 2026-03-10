from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db_main import Base

class Recyclables(Base):
    __tablename__ = 'add_recyclables'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    organic = Column(Float, default=0.0)
    paper = Column(Float, default=0.0)
    plastic = Column(Float, default=0.0)
    glass = Column(Float, default=0.0)
    metal = Column(Float, default=0.0)

    user = relationship("User", back_populates="recyclables")