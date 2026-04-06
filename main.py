from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db_main import engine, Base
from models.user import User
from models.user_total_recycled import UserTotalRecycled
from models.company import Company
from models.Add_Recyclable import Recyclables
from models.Recyclables import Recyclable_Item

from routers.recyclables_in import router as recyclables_router
from routers.recycling import router as dashboard_router
from routers import signup, login, company_signup, company_selection, testroute#, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signup.router)
app.include_router(login.router)
app.include_router(company_signup.router)
app.include_router(recyclables_router)
app.include_router(company_selection.router)
app.include_router(dashboard_router)
app.include_router(testroute.router)
#app.include_router(auth.router)
app.mount("/static", StaticFiles(directory=".", html=True), name="static")
@app.get("/")
def home():
    return {"message": "Server is running"}