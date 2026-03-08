from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import signup, login, company_signup
from db_main import engine, Base
from models.user import User
from models.user_home_link import User_Home
from models.company import Company
from models.Add_Recyclable import Recyclables
from models.Recyclables import Recyclable_Item 
from routers.recyclables_in import router 
Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)
origins = ["http://127.0.0.1:5500", "http://localhost:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(signup.router)
app.include_router(login.router)
app.include_router(company_signup.router)
app.include_router(router) # raouf hay router 8er ana msamiha hayk 
@app.get("/")
def home():
    return {"message": "Server is running"}