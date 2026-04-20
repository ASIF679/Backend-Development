from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from Database import get_db, engine
import models

# Create all database tables
models.Base.metadata.create_all(bind=engine)
# Initialize FastAPI app
app = FastAPI()
from auth_routes import router as auth_router
# Root route to confirm API is running
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "FastAPI is connected to Supabase DB!"}
app.include_router(auth_router)
