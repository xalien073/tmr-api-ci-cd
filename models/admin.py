#models/admin.py
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr

class Admin(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Vinod Borate",
                "email": "borate@tti.com",
                "password": "3xt3m#",
            }
        }

    class Settings:
        name = "admin"

class AdminSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "borate@tti.com", "password": "3xt3m#"}
        }

class AdminData(BaseModel):
    name: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "ame": "Vinod Borate",
                "email": "borate@tti.com",
            }
        }
