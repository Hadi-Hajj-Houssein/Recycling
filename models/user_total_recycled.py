from sqlalchemy import Column, String, Integer, UniqueConstraint, ForeignKey , Float
from sqlalchemy.orm import relationship
from db_main import Base
class UserTotalRecycled(Base):
    __tablename__ = 'user_total_recycled'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    total_organic = Column(Float, default=0.0)
    total_paper = Column(Float, default=0.0)
    total_plastic = Column(Float, default=0.0)
    total_glass = Column(Float, default=0.0)
    total_metal = Column(Float, default=0.0)
    user = relationship("User", back_populates="total_recycled")