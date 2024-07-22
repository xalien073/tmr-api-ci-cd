# routes/user.py
from fastapi import Body, APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models.user import User, NewUser, UserRoleEnum, UserSignIn, AssociatedUser, UpdatePassword
from config.config import get_database, create_user, get_user_by_email
from passlib.context import CryptContext
from auth.jwt_handler import sign_jwt
from typing import List

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

# @router.get("/users/{user_email}", response_model=NewUser)
# async def read_user(user_email: str, db=Depends(get_database)):
#     user = await get_user_by_email(db, user_email)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     user_id_str = str(user.pop('_id'))
#     return NewUser(id=user_id_str, **user)

@router.get("/users", response_model=List[NewUser])
async def users(db: AsyncIOMotorClient = Depends(get_database)):
    user_collection = db["user"]
    users = await user_collection.find().to_list(100)
    for user in users:
        user["id"] = str(user.pop("_id"))
        # Change _id to id and convert value to str
    usersList = [NewUser(**user) for user in users]
    print('users are', usersList)
    return usersList

@router.get("/associated-users", response_model=List[AssociatedUser])
async def associated_users(db: AsyncIOMotorClient = Depends(get_database)):
    user_collection = db["associated_users"]
    users = await user_collection.find().to_list(100)
    for user in users:
        user["id"] = str(user.pop("_id"))
        # Change _id to id and convert value to str
    usersList = [AssociatedUser(**user) for user in users]
    print('users are', usersList)
    return usersList

@router.post("/signup")#, response_model=NewUser)
async def create_user_route(user: User, db=Depends(get_database)):
    # Check for associated emails
    print(f'user.hideIdentity {user.hideIdentity}')
    associated_email = await get_user_by_email(db.associated_users, user.email)
    print(associated_email)
    if associated_email == None:
        raise HTTPException(status_code=400, detail="Email is not associated with the T T I.")

    existing_user = await get_user_by_email(db.user, user.email)
    print(f'existing_user {existing_user}')
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = hash_helper.encrypt(user.password)
    new_user = await create_user(db, user)
    token = sign_jwt(user.email)
    print(f'token is {token}, user email is {new_user["email"]}')
    return {
        "accessToken": token,
        "user": {
            "name": new_user["name"],
            "email": new_user["email"],
            "hideIdentity": new_user["hideIdentity"]
        }
    }
    
@router.post("/login")
async def login(credentials: UserSignIn = Body(...), db=Depends(get_database)):
    user_collection = db['user']
    user_exists = await user_collection.find_one({"email": credentials.username})
    print(f'user is {user_exists}')
    if user_exists:
        password = hash_helper.verify(credentials.password, user_exists['password'])
        if password:
            token = sign_jwt(credentials.username)
            print(f'token is {token}, user email is {user_exists["email"]}')
            return {
                "accessToken": token,
                "user": {
                    "name": user_exists["name"],
                    "email": user_exists["email"],
                    "hideIdentity": user_exists["hideIdentity"]
                }
            }

        raise HTTPException(status_code=403, detail="Incorrect email or password")

    raise HTTPException(status_code=403, detail="Incorrect email or password")

@router.post("/associated-users")
async def add_email(associated_user: AssociatedUser, db=Depends(get_database)):
    associated_users = db['associated_users']
    user_exists = await associated_users.find_one({"email": associated_user.email})
    print(f'user is {user_exists}')
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        await associated_users.insert_one(associated_user.dict())
        return {"message": "Email added successfully!", "email": associated_user.email}
    except Exception as e:
        # Handle database-related errors gracefully
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while adding the email: {str(e)}",
        )
    
@router.post("/change-password")
async def change_password(user: UpdatePassword, db=Depends(get_database)):
    user_collection = db['user']
    user_exists = await user_collection.find_one({"email": user.email})
    print(f'user is {user_exists}')
    if user_exists:
        new_password = hash_helper.encrypt(user.password)
        # Update the password in the database
        await user_collection.update_one(
            {"email": user.email},
            {"$set": {"password": new_password}}
        )
        return {"message": "Password updated successfully"}
    else:
        return {"error": "User not found"}
