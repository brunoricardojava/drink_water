from django.db import models

from .base_model import BaseModel
from .user_model import User


class UserDataHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
