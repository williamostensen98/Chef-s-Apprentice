from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100) #tenkt samme som tilhørende post
    ingredients = models.ManyToManyField(Ingredient, blank=False) #liste av ingrediensobjekter
    description = models.TextField() #tenkt sammen med content i post
    date_posted = models.DateTimeField(default=timezone.now)  # DateTimeField(auto_now=True) ville satt datoen til akkurat nå
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # on_delete=models.CASCADE sier at hvis brukeren blir slettet vil postene også bli slettet
    image = models.ImageField(default='default.jpg', upload_to='food_pics')
    visible = models.BooleanField(default=True)


    def __str__(self):
        return self.title

# class Post(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     ingredients = Recipe.ingredients
#     title = Recipe.title
#     description = Recipe.description
#     date_posted = Recipe.date_posted
#     author = Recipe.author
#
#     def __str__(self):
#         return self.title
