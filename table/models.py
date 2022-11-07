from django.db import models
from datetime import date, datetime


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()

    class Meta :
        indexes = [
            models.Index(fields=['birthday', ])
        ]

