# routes/review.py
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from models.review import Review
from config.config import get_database, get_current_user
from bson import ObjectId

router = APIRouter()

@router.post("/reviews/{meal_id}", response_model=Review)
async def create_review(meal_id: str, review: Review, db: AsyncIOMotorClient = Depends(get_database)):#, current_user: dict = Depends(get_current_user)):
    meals_collection = db["meal"]
    review_dict = review.dict()
    review_id = str(ObjectId())
    review_dict["id"] = review_id
    await meals_collection.update_one({"_id": ObjectId(meal_id)}, {"$push": {"reviews": review_dict}})
    return {**review.dict()}
