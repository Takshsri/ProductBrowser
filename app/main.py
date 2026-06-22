from fastapi import FastAPI
from app.routes.products import router
from app.routes.ui import router
app = FastAPI(
    title="Product Browser API"
)
app.include_router(router)
app.include_router(router)
@app.get("/")
def home():
    return {
        "message":"API Running successfully"
    }