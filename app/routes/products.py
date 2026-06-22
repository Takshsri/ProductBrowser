from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from app.database import get_db
from app.models import Product
from app.schemas import ProductPage

router = APIRouter(tags=["Products"])


@router.get("/products",response_model=ProductPage)
def get_products(
    limit: int = Query(default=20, le=100),
    cursor_updated_at: str | None = None,
    cursor_id: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Product)

    if category:
        query = query.filter(
            Product.category == category
        )

    if cursor_updated_at and cursor_id:

        cursor_time = datetime.fromisoformat(
            cursor_updated_at
        )

        query = query.filter(
            or_(
                Product.updated_at < cursor_time,

                and_(
                    Product.updated_at == cursor_time,
                    Product.id < cursor_id
                )
            )
        )

    products = (
        query
        .order_by(
            Product.updated_at.desc(),
            Product.id.desc()
        )
        .limit(limit + 1)
        .all()
    )

    has_next = len(products) > limit

    products = products[:limit]

    next_cursor = None

    if has_next:

        last_product = products[-1]

        next_cursor = {
            "updated_at":
            last_product.updated_at.isoformat(),

            "id":
            last_product.id
        }

    return {
        "products": products,
        "next_cursor": next_cursor
    }