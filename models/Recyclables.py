from sqlalchemy import Column,Integer,Float,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db_main import Base
# now =datetime.now()
class Recyclable_Item(Base):
    __tablename__ = 'recyclable_items'
    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(Integer, ForeignKey('users.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    type      = Column(String, nullable=False)
    name      = Column(String, nullable=False)
    desc      = Column(String, default='')
    weight    = Column(Float,  default=0.0)
    condition = Column(String, default='clean')
    status    = Column(String, default='pending')
    date      = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="recyclable_items")
    company = relationship("Company", back_populates="assigned_items")