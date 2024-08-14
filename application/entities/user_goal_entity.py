from pydantic import BaseModel
from datetime import date
from typing import List


class UserGoalEntity(BaseModel):
    date : date
    action: str
    user_goal: float
    total_quantity: float
    is_complete_goal: bool

class UserGoalEntityList(BaseModel):
    items: List[UserGoalEntity]
