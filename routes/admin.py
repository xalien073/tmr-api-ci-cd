#routes/admin.py
from fastapi import Body, APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from auth.jwt_handler import sign_jwt
from config.config import get_database, create_admin
from models.admin import Admin, AdminData, AdminSignIn
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

@router.post("/admin-signup")#, response_model=AdminData)
async def admin_signup(admin: Admin, db: AsyncIOMotorClient = Depends(get_database)):
    admins_collection = db["admin"]
    admin_exists = await admins_collection.find_one({"email": admin.email})
    if admin_exists:
        raise HTTPException(
            status_code=409, detail="Admin with email supplied already exists"
        )

    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await create_admin(db, admin)
    token = sign_jwt(admin.email)
    print(f'token is {token}, admin email is {new_admin["email"]}')
    return {
        "accessToken": token,
        "user": {
            "name": new_admin["name"],
            "email": new_admin["email"]
        }
    }

@router.post("/admin-login")
async def admin_login(admin_credentials: AdminSignIn = Body(...), db: AsyncIOMotorClient = Depends(get_database)):
    admins_collection = db["admin"]
    admin_exists = await admins_collection.find_one({"email": admin_credentials.username})
    if admin_exists:
        password = hash_helper.verify(admin_credentials.password, admin_exists['password'])
        if password:
            token = sign_jwt(admin_credentials.username)
            print(f'token is {token}, user email is {admin_credentials.username}')
            return {
                "accessToken": token,
                "user": {
                    "name": admin_exists["name"],
                    "email": admin_exists["email"]
                }
            }

        raise HTTPException(status_code=403, detail="Incorrect email or password")

    raise HTTPException(status_code=403, detail="Incorrect email or password")
