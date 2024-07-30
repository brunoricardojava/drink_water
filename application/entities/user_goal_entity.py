from pydantic import BaseModel


class UserGoalEntity(BaseModel):
    action: str
    user_goal: float
    total_quantity: float
    is_complete_goal: bool
