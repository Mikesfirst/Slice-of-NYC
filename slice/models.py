from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE  

# Create your models here.
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, default=999)
#     name = models.CharField(max_length=100, null=True, blank=True)
#     birthday = models.DateField(null=True, blank=True)
#     email = models.CharField(max_length=100, null=True, blank=True)
#     food_pref = models.CharField(max_length=500, null=True, blank=True)
#     personality = models.CharField(max_length=500, null=True, blank=True)
#     interests = models.CharField(max_length=500, null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    food_pref = models.CharField(max_length=255, null=True, blank=True)
    interests = models.CharField(max_length=255, null=True, blank=True)
    date_of_plan = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    hunger_level = models.CharField(max_length=255, null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    boroughs = models.CharField(max_length=255, null=True, blank=True)
    models.ExpressionList

    




    def __str__(self):
        return self.name

