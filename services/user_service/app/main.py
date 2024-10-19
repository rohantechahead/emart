import os
import sys

from fastapi import FastAPI

from common.database import engine
from .models import Base
from .routes import router as user_router

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include user routes
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
