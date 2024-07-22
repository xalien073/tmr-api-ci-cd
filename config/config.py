#config.py
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import status, Depends, HTTPException
from jose import JWTError, jwt
from auth.jwt_handler import decode_jwt
import os

# MongoDB Configuration
MONGO_URI = os.getenv("DATABASE_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Dependency to get the MongoDB client
async def get_database():
    client = AsyncIOMotorClient(MONGO_URI)
    database = client[DATABASE_NAME]
    return database

async def create_admin(db, new_admin):
    admin_collection = db["admin"]
    admin = await admin_collection.insert_one(new_admin.dict())
    response_data = new_admin.dict()
    return response_data

async def create_user(db, new_user):
    user_collection = db["user"]
    user = await user_collection.insert_one(new_user.dict())
    # user_id = str(user.inserted_id)
    response_data = new_user.dict()
    # response_data["id"] = str(user_id)
    # return NewUser(**response_data)
    return response_data
    
async def get_user_by_email(db, email: str):
    return await db.find_one({"email": email})

async def get_current_admin_user(token: str = Depends(decode_jwt),
                                 db: AsyncIOMotorClient = Depends(get_database)):
    print(f'checking for current user')
    print(f'token is {token}')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    # Extract the email from the decoded token
    print(f'email in token is {token.get("user_id")}')
    email = token.get("user_id")
    # Check if the user with the given email exists in the admin collection
    admin = await Admin.find_one({"email": email})
    if admin:
        return admin
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. User is not an admin.",
        )

async def get_current_user(token: str = Depends(decode_jwt),
                                 db: AsyncIOMotorClient = Depends(get_database)):
    print(f'checking for current user')
    print(f'token is {token}')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    users = db["user"]
    # Extract the email from the decoded token
    print(f'email in token is {token.get("user_id")}')
    email = token.get("user_id")
    # Check if the user with the given email exists in the admin collection
    user = await users.find_one({"email": email})
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Invalid token",
        )
    