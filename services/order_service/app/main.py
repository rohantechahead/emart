import os
import sys
# Keep this import first
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from fastapi import FastAPI
from common.database import engine
from services.order_service.app.models import OrderServiceBase
from .routes import router as order_router

app = FastAPI()

OrderServiceBase.metadata.create_all(bind=engine)

app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
