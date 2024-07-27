from django.db import models

from .base_model import BaseModel
from .user_model import User


class Action(BaseModel):
    POSSIBLE_ACTIONS = {
        ("DRINK WATER","DRINK WATER")
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    action = models.CharField(choices=POSSIBLE_ACTIONS, default="DRINK WATER", max_length=30, db_index=True)
    quantity = models.FloatField()
