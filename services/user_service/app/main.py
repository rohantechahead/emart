import os
import sys

from fastapi import FastAPI

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from common.database import engine
from .models import Base
from .routes import router as user_router

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include user routes
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
