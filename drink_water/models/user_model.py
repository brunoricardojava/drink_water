from django.db import models

from .base_model import BaseModel


class User(BaseModel):
    name = models.CharField()
    weight = models.FloatField(null=True, blank=True)
