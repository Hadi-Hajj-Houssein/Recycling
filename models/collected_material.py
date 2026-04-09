from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow your frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pickups = []

@app.get("/pickups")
def get_pickups():
    return pickups

@app.post("/pickups")
def add_pickup(pickup: dict):
    pickups.insert(0, pickup)
    return {"message": "added"}