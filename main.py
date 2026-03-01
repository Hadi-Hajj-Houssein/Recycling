from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 1. IMPORT THE ROUTERS
from routers import signup, login 
from db_main import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Setup (Keep this)
origins = ["http://127.0.0.1:5500", "http://localhost:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. CONNECT THE ROUTERS (CRITICAL STEP)
# If these lines are missing or commented out, you get 404 Error.
app.include_router(signup.router)
app.include_router(login.router)

@app.get("/")
def home():
    return {"message": "Server is running"}