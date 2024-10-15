from fastapi import FastAPI
from common.database import engine
from .models import Base
from .routes import router as product_router

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

app.include_router(product_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
