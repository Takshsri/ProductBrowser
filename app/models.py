from sqlalchemy import Column,String,DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    name = Column(String,nullable=False)
    category = Column(String,nullable=False)
    created_at = Column(
        DateTime,
        default = datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        default = datetime.utcnow
    )