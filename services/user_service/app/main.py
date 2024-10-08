<<<<<<< HEAD

=======
>>>>>>> 653c0d1a5799922e77f6f729785c11821bb6287c
from fastapi import FastAPI

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

    uvicorn.run(app, host="127.0.0.1", port=8000)
<<<<<<< HEAD

=======
>>>>>>> 653c0d1a5799922e77f6f729785c11821bb6287c
