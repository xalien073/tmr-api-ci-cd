# models/review.py
from pydantic import BaseModel, conint, Field

class Review(BaseModel):
    reviewer: dict = Field(..., example={"name": "John Doe", "email": "johndoe@example.com", "hideIdentity": False})
    rating: conint(ge=0, le=5)
    review: str
