from django.db import models

from .base_model import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=50, db_index=True)
    weight = models.FloatField()
