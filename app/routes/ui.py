from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from app.database import get_db
from app.models import Product

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(
    request: Request,
    category: str | None = None,
    cursor_updated_at: str | None = None,
    cursor_id: str | None = None,
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
        .limit(21)
        .all()
    )

    next_cursor = None

    if len(products) > 20:

        last_product = products[19]

        next_cursor = {
            "updated_at": last_product.updated_at.isoformat(),
            "id": last_product.id
        }

        products = products[:20]

    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={
            "products": products,
            "category": category,
            "next_cursor": next_cursor
        }
    )