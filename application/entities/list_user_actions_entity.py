from datetime import date
from typing import Optional
from pydantic import BaseModel


class ListUserActionsEntity(BaseModel):
    user_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
