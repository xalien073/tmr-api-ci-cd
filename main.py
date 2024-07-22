# app/app.py
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routes import admin, user, meal, review
from auth.jwt_bearer import JWTBearer
from fastapi.middleware.cors import CORSMiddleware

import os

import os

def read_config_data(filename):
    filepath = os.path.join("/app/cm", filename)
    try:
        with open(filepath, "r", os.O_NOATIME) as f:  # Open with O_NOATIME flag
            return f.read()
    except FileNotFoundError:
        # Handle potential file not found error (optional)
        return None  # Or raise an exception based on your application logic

# def read_config_data2(filename):
#     filepath = os.path.join("/app/cm", filename)
#     try:
#         with open(filepath, "r") as f:
#             data = f.read()
#             f.seek(0)  # Move the file pointer to the beginning
#             f.truncate()  # Clear the buffer
#             return data
#     except FileNotFoundError:
#         # Handle potential file not found error (optional)
#         return None  # Or raise an exception based on your application logic

cm_test = read_config_data("TEST")
cm_port = read_config_data("PORT")
cm_url = read_config_data("URL")

token_listener = JWTBearer()

app = FastAPI()

origins = [
    "http://localhost:3000",  # Allow requests from localhost 3000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def read_root():
    print(cm_test)
    print(cm_port)
    print(cm_url)
    return {
        "message": "Welcome to T T I Meal Reviewer!.",
        "test": cm_test,
        "port": cm_port,
        "url": cm_url
        }

# Include routers from different files
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(meal.router)
app.include_router(review.router)
