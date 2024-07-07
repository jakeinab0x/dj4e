from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Breed(models.Model):
    name = models.CharField(
        max_length=200,
        validators=MinLengthValidator[(2, "Breed must have at least two characters.")]
        )

    def __str__(self):
        return self.name

class Cat(models.Model):
    nickname = models.CharField(
        max_length=200,
        validators=MinLengthValidator[(2, "Nickname must have at least two characters.")]
        )
    weight = models.PositiveIntegerField()
    foods = models.CharField(max_length=300)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
