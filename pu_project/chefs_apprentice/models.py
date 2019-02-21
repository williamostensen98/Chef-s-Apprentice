from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) #DateTimeField(auto_now=True) ville satt datoen til akkurat nå
    author = models.ForeignKey(User, on_delete=models.CASCADE) #on_delete=models.CASCADE sier at hvis brukeren blir slettet vil postene også bli slettet

    def __str__(self):
        return self.title


class Ingredient (models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(blank=False) #Må settes en mengde
    units = ( #forskjellige enheter fra scrollmeny
        ('liter', 'liter'),
        ('dl', 'dl'),
        ('ss', 'ss'),
        ('ts', 'ts'),
        ('kg', 'kg'),
        ('gram', 'gram'),
        ('boks', 'boks'),
    )
    unit = models.CharField(choices=units, max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Recipe (models.Model):
    title = models.CharField(max_length=100) #tenkt samme som tilhørende post
    ingredients = models.ManyToManyField(Ingredient, blank=False) #liste av ingrediensobjekter
    description = models.TextField() #tenkt sammen med content i post

    def __str__(self):
        return self.title
