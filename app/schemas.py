from pydantic import BaseModel
from datetime import datetime


class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductPage(BaseModel):
    products: list[ProductResponse]
    next_cursor: dict | None