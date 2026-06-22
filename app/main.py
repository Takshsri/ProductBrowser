from fastapi import FastAPI
from app.routes.products import router as products_router
from app.routes.ui import router as ui_router
app = FastAPI(
    title="Product Browser API"
)
app.include_router(products_router)
app.include_router(ui_router)
@app.get("/health")
def health():
    return {
        "message":"API Running successfully"
    }