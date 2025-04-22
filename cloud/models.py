from sqlalchemy import Column, Integer, String
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)