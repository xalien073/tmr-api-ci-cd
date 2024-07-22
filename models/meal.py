# models/meal.py
from datetime import datetime
from typing import List
from enum import Enum
from pydantic import BaseModel
from .review import Review

class MealTypeEnum(str, Enum):
    breakfast = "Breakfast"
    lunch = "Lunch"
    snack = "Snack"
    dinner = "Dinner"

class Meal(BaseModel):
    name: str
    current_date: str = str(datetime.utcnow().date())
    current_day: str = datetime.utcnow().strftime('%A')
    meal_type: MealTypeEnum
    reviews: list[Review]
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Tea",
                "current_date": str(datetime.utcnow().date()),
                "current_day": datetime.utcnow().strftime('%A'),
                "meal_type": "Breakfast",
                "reviews": []
            }
        }

class MealResponse(BaseModel):
    id: str
    name: str
    current_date: str
    current_day: str
    meal_type: MealTypeEnum
    reviews: list[Review]  # Include reviews
