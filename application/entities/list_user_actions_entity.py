from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ListUserActionsEntity(BaseModel):
    user_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
