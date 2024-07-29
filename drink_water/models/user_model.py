from django.db import models

from .base_model import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=50, db_index=True)
    weight = models.FloatField()

    def __str__(self) -> str:
        return f"{self.name} - {self.id}"
