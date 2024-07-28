from django.db import models

from .base_model import BaseModel
from .user_model import User


class UserAction(BaseModel):
    POSSIBLE_ACTIONS = ["DRINK WATER"]

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    action = models.CharField(default="DRINK WATER", max_length=30, db_index=True)
    quantity = models.FloatField()
