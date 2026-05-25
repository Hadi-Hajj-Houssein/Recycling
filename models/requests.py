from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_main import Base


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    recyclable_item_id = Column(
        Integer,
        ForeignKey("recyclable_items.id"),
        index=True,
        nullable=False
    )
    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        index=True  
    )

    company = relationship("Company", back_populates="requests")