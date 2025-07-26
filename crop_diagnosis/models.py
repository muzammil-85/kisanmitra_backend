
from django.db import models

class VegetableEntry(models.Model):
    class Meta:
        verbose_name = "Vegetable"
        verbose_name_plural = "Vegetables"

    def __str__(self):
        return "Firestore Vegetable Entry"