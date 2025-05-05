from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

# SQLAlchemy Modell
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

# Pydantic Modelle
#class EncryptedPayload(BaseModel):
#    enc: str
#    ciphertext: str

#class ItemCreate(BaseModel):
#    encrypted_data: EncryptedPayload

class ItemCreatePlain(BaseModel):
    name: str
    description: str