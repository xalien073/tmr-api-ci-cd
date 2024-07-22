# models/user.py
from enum import Enum
from pydantic import BaseModel, EmailStr, constr
from fastapi.security import HTTPBasicCredentials

class UserRoleEnum(str, Enum):
    staff = "staff"
    student = "student"

class User(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8) # Minimum password length of 8 characters
    role: UserRoleEnum
    hideIdentity: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Vinod Borate",
                "email": "borate@tti.com",
                "password": "3xt3m#$%",
                "role": "staff",
                "hideIdentity": False,
            }
        }

class NewUser(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRoleEnum

class UserSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "borate@tti.com", "password": "3xt3m#$%"}
        }
        
class AssociatedUser(BaseModel):
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "borate@tti.com",
            }
        }

class UpdatePassword(BaseModel):
    email: EmailStr
    password: constr(min_length=8) # Minimum password length of 8 characters

    class Config:
        json_schema_extra = {
            "example": {
                "email": "borate@tti.com",
                "password": "3xt3m#$%",
            }
        }