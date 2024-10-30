import os
import sys

# keep this import first
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from fastapi import FastAPI
from common.database import engine
from services.product_service.app.models import ProductServiceBase
from .routes import router as product_router

app = FastAPI()

ProductServiceBase.metadata.create_all(bind=engine)

app.include_router(product_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
