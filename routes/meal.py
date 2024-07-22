# routes/meal.py
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError
from models.meal import Meal, MealResponse
from models.admin import Admin
from config.config import get_database#, get_current_admin_user
from bson import ObjectId
from typing import List

router = APIRouter()

# @router.get("/meals/{meal_id}", response_model=Meal)
# async def read_meal(meal_id: str, db: AsyncIOMotorClient = Depends(get_database)):
#     meals_collection = db["meal"]
#     document = await meals_collection.find_one({"_id": ObjectId(meal_id)})
#     if document:
#         meal = Meal(**document)  # Convert MongoDB document to Meal model
#         return meal
#     raise HTTPException(status_code=404, detail="Meal not found")

@router.get("/latest-meals", response_model=List[MealResponse])
async def read_latest_meals(db: AsyncIOMotorClient = Depends(get_database)):
    meals_collection = db["meal"]
    # Retrieve meals with _id projection
    latest_meals = await meals_collection.find({}, {"_id": 1, "name": 1, "current_date": 1, "current_day": 1, "meal_type": 1, "reviews": 1}).sort("_id", -1).limit(8).to_list(8)
    for meal in latest_meals:
        meal["id"] = str(meal.pop("_id"))  # Change _id to id and convert value to str
    # Create ListMealResponse objects
    meals = [MealResponse(**meal) for meal in latest_meals]
    print('meals are', meals)
    return meals # _id will be included in the response

@router.post("/meals", response_model=MealResponse)
async def create_meal(meal: Meal,
                      db: AsyncIOMotorClient = Depends(get_database),
                    #   current_admin_user: Admin = Depends(get_current_admin_user)
                      ):
    meals_collection = db["meal"]
    result = await meals_collection.insert_one(meal.dict())
    meal_id = result.inserted_id
    # Create a new response dictionary with the ID and meal attributes
    response_data = meal.dict()
    response_data["id"] = str(meal_id)
    return MealResponse(**response_data)  # Create MealResponse from dict

@router.patch("/meals/{meal_id}", response_model=Meal)
async def update_meal(
    meal_id: str,
    mealName: str,
    db: AsyncIOMotorClient = Depends(get_database)
):
    print('patch request ran')
    try:
        meal_id = ObjectId(meal_id)  # Ensure valid object ID
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid meal ID")

    meals_collection = db["meal"]
    # Use update_one with dictionary unpacking for selective update
    update_data = {"$set": {"name": mealName}}
    result = await meals_collection.update_one({"_id": meal_id}, update_data)

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Meal not found")

    # Fetch the updated document directly (optional)
    updated_meal = await meals_collection.find_one({"_id": meal_id})
    return updated_meal
